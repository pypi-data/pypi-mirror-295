import pprint

from web3 import AsyncWeb3
from web3.types import TxParams
from web3._utils.async_transactions import (
    async_fill_nonce,
    async_fill_transaction_defaults,
)

from .data_types import Token
from .utility import make_token_contract


async def fill_transaction_defaults(w3: AsyncWeb3, transaction: TxParams) -> TxParams:
    transaction = await async_fill_nonce(w3, transaction)
    return await async_fill_transaction_defaults(w3, transaction)


async def send_transaction(
    w3: AsyncWeb3, private_key, transaction: TxParams, identifier: str
) -> None:
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = await w3.eth.send_raw_transaction(
        signed_transaction.raw_transaction
    )

    print(f"Hash for {identifier}: {transaction_hash.hex()}")

    transaction_receipt = await w3.eth.wait_for_transaction_receipt(transaction_hash)

    print(f"Received receipt for {identifier}:")
    pprint.pprint(dict(transaction_receipt))

    if transaction_receipt["status"] != 0x1:
        print(f"{identifier} transaction failed")

    print(f"Transaction success for {identifier}")


async def transfer_token(
    w3: AsyncWeb3, token: Token, amount: int, public_key, private_key, wallet
) -> None:
    assert token.symbol != "ETH", "Token must be ERC-20 token, not gas token"

    if amount <= 0:
        print(f"Skipping {token} - balance empty")
        return

    print(f"Transferring {amount} units of {token}")

    contract = make_token_contract(w3, token)
    nonce = await w3.eth.get_transaction_count(public_key)

    transaction = await contract.functions.transfer(wallet, amount).build_transaction(
        {
            "chainId": token.chain.id,
            "from": public_key,
            "nonce": nonce,
        }
    )

    await send_transaction(w3, private_key, transaction, str(token))
