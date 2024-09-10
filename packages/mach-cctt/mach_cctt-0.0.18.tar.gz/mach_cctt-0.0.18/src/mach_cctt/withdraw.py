import asyncio
import pprint

from web3 import AsyncWeb3
from web3.middleware import ExtraDataToPOAMiddleware

from .client import client
from . import config
from .data_types import Token
from .transfers import fill_transaction_defaults, send_transaction, transfer_token


async def drain_eth(w3: AsyncWeb3, chain: str, public_key, private_key, wallet) -> None:
    # TODO
    print(f"Warning: skipping {chain}-ETH: not currently draining gas tokens")
    return

    identifier = f"{chain}-ETH"

    print(f"Withdrawing {identifier}")

    # TODO: This does not currently account for L1 fees for Optimism, which will thus fail
    # https://docs.optimism.io/stack/transactions/fees
    # https://github.com/ethereum/web3.py/issues/3079

    transaction = await fill_transaction_defaults(
        w3,
        {
            "from": public_key,
            "to": wallet,
            "type": 2,  # EIP-1559
        },
    )

    gas = transaction["gas"]
    max_fee_per_gas = transaction["maxFeePerGas"]
    total_gas_cost = w3.to_wei(gas * max_fee_per_gas, "wei")

    balance = await w3.eth.get_balance(public_key)
    value = w3.to_wei(max(0, balance - total_gas_cost), "wei")

    print(f"{identifier} balance of {balance}")
    print(f"{identifier} gas of {gas}")
    print(f"{identifier} max fee per gas of {max_fee_per_gas}")
    print(f"{identifier} total gas cost of {total_gas_cost}")
    print(f"{identifier} transaction value would be {value}")

    if value <= 0:
        print(f"Skipping {identifier}")
        return

    transaction["value"] = value

    await send_transaction(w3, private_key, transaction, identifier)


# Drains balances of all tokens and ETH on the chain into the destination wallet
# async def drain_chain(tokens: Sequence[Token], public_key, private_key, wallet) -> None:
async def drain_chain(
    chain: str, balances: dict[str, int], public_key, private_key, wallet
) -> None:
    print(f"Draining {chain}")

    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(config.rpc_urls[chain]))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # First drain everything but the gas token
    await asyncio.gather(
        *(
            transfer_token(
                w3,
                Token.from_components(chain, symbol),
                balance,
                public_key,
                private_key,
                wallet,
            )
            for symbol, balance in filter(
                lambda item: item[0] != "ETH", balances.items()
            )
        )
    )

    # Then drain the gas token
    await drain_eth(w3, chain, public_key, private_key, wallet)


async def drain_all(public_key, private_key, wallet) -> None:
    all_balances = client.get_token_balances(public_key)

    print("Balances:")
    pprint.pprint(all_balances)

    await asyncio.gather(
        *(
            drain_chain(chain, balances, public_key, private_key, wallet)
            for chain, balances in all_balances.items()
        )
    )
