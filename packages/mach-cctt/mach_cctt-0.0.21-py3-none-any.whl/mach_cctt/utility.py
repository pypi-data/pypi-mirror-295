import datetime
import logging
import sys
from pathlib import Path
import random
from typing import AbstractSet, Optional

from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from .client import client
from . import config
from .data_types import Token


def make_logger(name: str, path: Optional[Path], exclusive=False) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler: logging.Handler = logging.FileHandler(path) if path else logging.StreamHandler(sys.stdout)  # type: ignore
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if path and not exclusive:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    logger.info(f"START {datetime.datetime.today()}\n")

    return logger


def make_w3_from_token(token: Token) -> AsyncWeb3:
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(token.chain.rpc_url))

    if not w3.is_checksum_address(token.contract_address):
        raise ValueError("Invalid Params")

    imported_account = w3.eth.account.from_key(config.private_key)
    w3.eth.default_account = imported_account.address

    return w3


def make_token_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=AsyncWeb3.to_checksum_address(token.contract_address),
        abi=config.erc20_abi,
    )


def make_order_book_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=client.deployments[token.chain.name]["contracts"]["order_book"],
        abi=config.order_book_abi,
    )


# TODO: Annotate with generics in Python 3.12+
def random_set_choice(s: AbstractSet[str]) -> str:
    return random.choice(tuple(s))


def choose_source_token(
    excluded_chains: AbstractSet[str], wallet_address: ChecksumAddress
) -> Token:
    balances = client.get_token_balances(wallet_address)

    token: Optional[tuple[int, str, str]] = None

    # Choose the token with the greatest balance (regardless of denomination) that is not the gas token
    for chain, chain_balances in filter(
        lambda item: item[0] not in excluded_chains, balances.items()
    ):
        for symbol, balance in chain_balances.items():
            if client.gas_tokens.get(chain, None) != symbol and (not token or token[0] < balance):
                token = (balance, chain, symbol)

    if not token:
        raise RuntimeError("No viables source tokens to choose from")

    return Token.from_components(token[1], token[2])
