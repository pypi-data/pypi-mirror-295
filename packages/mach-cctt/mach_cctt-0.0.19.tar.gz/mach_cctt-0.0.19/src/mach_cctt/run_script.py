import asyncio
import logging
from pathlib import Path
from pprint import pformat
import time
from typing import Optional

from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from .balances import get_balance, get_gas_balance
from .client import client
from . import config
from .data_types import Token
from .destination_policy import DestinationPolicy
from .transactions import safe_build_and_send_tx
from .utility import (
    choose_source_token,
    make_logger,
    make_order_book_contract,
    make_w3_from_token,
)

logger = logging.getLogger("cctt")


def initialize_config(private_key: HexBytes) -> None:
    assert "production" in config.backend_url, "Backend URL should point to production"
    config.private_key = private_key.hex().removeprefix("0x")


async def ensure_approval(
    w3: AsyncWeb3, public_address, spender_address, src_address, amount: int
) -> Optional[HexBytes]:
    contract: AsyncContract = w3.eth.contract(address=src_address, abi=config.erc20_abi)

    try:
        allowance_func = contract.functions.allowance(
            public_address,
            spender_address,
        )
    except Exception as e:
        raise ValueError(f"failed to build allowance function: {e}") from e

    try:
        allowance: int = await allowance_func.call()
    except Exception as e:
        raise ConnectionError(f"failed to get allowance: {e}") from e

    logger.info(f"Allowance of {allowance=}/{amount=} ({100 * allowance / amount}%)")

    if allowance >= amount:
        return None

    try:
        approve_func = contract.functions.approve(
            spender_address,
            amount,
        )
    except Exception as e:
        raise ValueError(f"failed to build approve function: {e}") from e

    logger.info("Approving larger allowance")
    try:
        tx_hash = await safe_build_and_send_tx(
            w3,
            config.private_key,
            public_address,
            approve_func,
        )
    except Exception as e:
        raise ValueError(f"failed to send approve tx: {e}") from e

    logger.info(f"Approval transaction hash: {tx_hash.hex()}")
    return tx_hash


async def test_bounce_trade(src_token: Token, destination_policy: DestinationPolicy):
    src_w3 = make_w3_from_token(src_token)
    src_order_book_contract = make_order_book_contract(src_w3, src_token)

    delayed_transaction_logger = make_logger(
        "delayed_transactions", Path(config.log_files["delayed_transactions"]), True
    )
    stuck_transaction_logger = make_logger(
        "stuck_transactions", Path(config.log_files["stuck_transactions"]), True
    )
    improper_fill_logger = make_logger(
        "stuck_transactions", Path(config.log_files["improper_fills"]), True
    )

    excluded_chains: set[str] = set()
    destination_policy.add_tried_chain(src_token.chain)

    while True:
        logger.debug("")

        initial_src_balance = await get_balance(src_w3, src_token)

        logger.debug(f"{initial_src_balance=}")
        
        # TODO: we seemingly can never fill 1 tick, treat it as 0
        if initial_src_balance <= 1:
            logger.critical(f"Insufficient source balance! Cannot continue trading")
            break

        dest_token = destination_policy()
        destination_policy.add_tried_token(dest_token)
        dest_w3 = make_w3_from_token(dest_token)

        logger.info(f"Swapping {src_token} for {dest_token}")

        if await get_gas_balance(dest_w3) <= 0:
            logger.info(
                f"No gas on chain {dest_token.chain.name}, will be excluded from future selection"
            )
            destination_policy.exclude_chain(dest_token.chain)
            excluded_chains.add(dest_token.chain.name)
            continue

        try:
            quote = client.request_quote(
                src_token,
                dest_token,
                initial_src_balance,
                src_w3.eth.default_account,  # type: ignore
            )
        except Exception as e:
            logger.warning(f"Quote request failed: {e}")
            continue

        logger.debug("Quote:")
        logger.debug(pformat(quote))

        assert (
            quote["src_asset_address"] == src_token.contract_address
        ), f"Need {quote['src_asset_address']=} to equal {src_token.contract_address=}"

        if quote["invalid_amount"]:
            logger.warning("Quote had invalid amount")
            continue

        src_amount, dest_amount = quote["src_amount"], quote["dst_amount"]

        logger.info(
            f"Can fill {src_amount=}/{initial_src_balance=} ({100 * src_amount / initial_src_balance}%)"
        )

        assert src_amount <= initial_src_balance

        if src_amount < initial_src_balance:
            logger.warning("Not enough liquidity to trade entire source balance")

            if src_amount <= 0:
                logger.warning(f"Trying another destination")
                break

        try:
            await ensure_approval(
                src_w3,
                src_w3.eth.default_account,
                src_order_book_contract.address,
                src_token.contract_address,
                src_amount,
            )
        except Exception as e:
            logger.critical(f"Failed to ensure approval")
            raise e

        try:
            order_direction = (
                src_token.contract_address,  # srcAsset: address
                dest_token.contract_address,  # dstAsset: address
                dest_token.chain.lz_cid,  # dstLzc: uint32
            )

            order_funding = (
                src_amount,  # srcQuantity: uint96
                dest_amount,  # dstQuantity: uint96
                quote["bond_fee"],  # bondFee: uint16
                quote["bond_asset_address"],  # bondAsset: address
                quote["bond_amount"],  # bondAmount: uint96
            )

            order_expiration = (
                int(time.time()) + 3600,  # timestamp: uint32
                quote["challenge_offset"],  # challengeOffset: uint16
                quote["challenge_window"],  # challengeWindow: uint16
            )

            is_maker = False

            place_order = src_order_book_contract.functions.placeOrder(
                order_direction,
                order_funding,
                order_expiration,
                is_maker,
            )

            gas_estimate = await place_order.estimate_gas(
                {
                    "from": src_w3.eth.default_account,  # type: ignore
                    "value": src_w3.to_wei(0, "wei"),
                }
            )
            gas_price = await src_w3.eth.gas_price
            logger.info(
                f"Estimated gas on {src_token.chain.name} of {gas_estimate} at price {gas_price}"
            )

            tx_hash = await safe_build_and_send_tx(
                src_w3,
                config.private_key,
                src_w3.eth.default_account,  # type: ignore
                place_order,
            )
            logger.info(f"Placed order with hash: {tx_hash.hex()}")

            tx_receipt = await src_w3.eth.wait_for_transaction_receipt(tx_hash)
            logger.debug("Receipt:")
            logger.debug(pformat(dict(tx_receipt)))

        except Exception as e:
            logger.warning(f"Failed to send the transaction: {e}")
            continue

        # These need to be computed before the order has been submitted
        start_dest_balance = await get_balance(dest_w3, dest_token)
        expected_src_balance = initial_src_balance - src_amount
        expected_dest_balance = start_dest_balance + dest_amount

        try:
            order_response = client.submit_order(src_token.chain.name, tx_hash.hex())

        except Exception as e:
            logger.warning(f"There was an error submitting this order: {e}")
            await asyncio.sleep(5)
            continue

        logger.info("Submitted order")
        logger.debug("Response:")
        logger.debug(pformat(order_response))

        count = 0
        logger.debug("Waiting for source balance to be withdrawn...")

        while (
            src_balance := await get_balance(src_w3, src_token)
        ) > expected_src_balance and count < config.max_polls:
            count += 1
            logger.debug(f"{src_balance=} > {expected_src_balance=}")

            # TODO
            if src_balance == expected_src_balance + 1:
                logger.warning(
                    "Improper fill of 1 tick less than quoted for. This is a known issue."
                )
                improper_fill_logger.warning(tx_hash)
                improper_fill_logger.warning(pformat(order_response) + "\n")
                break

            await asyncio.sleep(config.poll_timeout)

        if count >= config.max_polls:
            logger.warning(
                "Source balance not withdrawn after max waiting time. Retrying with a different destination token."
            )
            delayed_transaction_logger.warning(tx_hash)
            delayed_transaction_logger.warning(pformat(order_response) + "\n")
            continue

        count = 0
        logger.info("Source balance withdrawn, waiting to receive destination token...")

        while (
            dest_balance := await get_balance(dest_w3, dest_token)
        ) < expected_dest_balance and count < config.max_polls:

            count += 1

            logger.debug(f"{dest_balance=} < {expected_dest_balance=}")

            await asyncio.sleep(config.poll_timeout)

        if count >= config.max_polls:
            logger.warning("Exceeded max number of polls. Transaction possibly stuck.")
            stuck_transaction_logger.warning(tx_hash)
            stuck_transaction_logger.warning(pformat(order_response) + "\n")

            src_token = choose_source_token(
                excluded_chains, src_w3.eth.default_account  # type: ignore
            )
            src_w3 = make_w3_from_token(src_token)
            src_order_book_contract = make_order_book_contract(src_w3, src_token)

        else:
            logger.info("Destination balance received - order complete")

            src_token, src_w3, src_order_book_contract = (
                dest_token,
                dest_w3,
                make_order_book_contract(dest_w3, dest_token),
            )

        destination_policy.reset()
        destination_policy.add_tried_token(src_token)
        destination_policy.add_tried_chain(src_token.chain)
