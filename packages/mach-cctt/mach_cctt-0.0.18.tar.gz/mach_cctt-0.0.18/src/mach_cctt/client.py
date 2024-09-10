from collections.abc import Callable
import functools
import logging
from pprint import pformat
import requests
from typing import AbstractSet, Any, TypedDict

import eth_typing

from . import config


# Note: we should really just be deserializing the backend Quote type with BaseModel.validate_from_json
# - https://github.com/tristeroresearch/cache-half-full/blob/62b31212f0456e4fad564021289816d39345b49b/backend/api/v1/endpoints/quotes.py#L51
# - https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate_json
class Quote(TypedDict):
    wallet_address: str
    src_chain: str
    dst_chain: str
    src_amount: int
    dst_amount: int
    bond_amount: int
    bond_fee: int
    src_asset_address: str
    bond_asset_address: str
    challenge_offset: int
    challenge_window: int
    invalid_amount: bool
    liquidity_source: str
    created_at: str
    expires_at: str


class MachClient:
    # Routes
    orders = config.backend_url + config.endpoints["orders"]
    quotes = config.backend_url + config.endpoints["quotes"]
    token_balances = config.backend_url + config.endpoints["token_balances"]
    get_config = config.backend_url + config.endpoints["get_config"]

    def __init__(self, root_url: str = config.backend_url):
        self.root = root_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.logger = logging.getLogger("cctt")
        # Initialize the cached property
        self.deployments

    # TODO: Annotate return type with generics in Python 3.12+
    def _handle_response(
        self,
        response: requests.Response,
        on_success: Callable[[requests.Response], Any] = lambda r: r.json(),
    ) -> Any:
        match response.status_code:
            case 200:
                return on_success(response)

            case 422:
                self.logger.debug("Response:")
                self.logger.debug(pformat(response.json()))
                raise ValueError("Validation error: invalid request")

            case _:
                self.logger.debug("Response:")
                self.logger.debug(pformat(response.json()))
                raise RuntimeError(f"Unknown status code {response.status_code}")

    @functools.cached_property
    def deployments(self) -> dict:
        data: dict = {}

        response = self.session.get(
            MachClient.get_config,
            json=data,
        )

        deployments = self._handle_response(response)["deployments"]
        deployments = {chain: data for chain, data in deployments.items() if chain not in config.excluded_chains}

        for chain in frozenset(deployments.keys()) - frozenset(config.rpc_urls.keys()):
            self.logger.warn(f"{chain=} RPC URL missing from config")
            # Forbid chains for which we don't have the RPC URL
            del deployments[chain]

        self.gas_tokens_: dict[str, str] = {}

        for chain, data in deployments.items():
            for symbol, symbol_data in deployments[chain]["assets"].items():
                if symbol_data.get("wrapped"):
                    assert (
                        symbol not in self.gas_tokens_
                    ), f"Error: more than 1 gas token on {chain}: {self.gas_tokens_['chain']}, {symbol}"
                    self.gas_tokens_[chain] = symbol

        self.chains_ = frozenset(deployments.keys())

        return deployments

    @property
    def chains(self) -> frozenset:
        return self.chains_

    @property
    def gas_tokens(self) -> dict[str, str]:
        return self.gas_tokens_

    def symbols(self, chain: str) -> frozenset:
        return frozenset(self.deployments[chain]["assets"])

    def request_quote(
        self,
        src_token: "Token",  # type: ignore
        dest_token: "Token",  # type: ignore
        src_amount: int,
        wallet: eth_typing.ChecksumAddress,
    ) -> Quote:
        data = {
            "dst_asset_address": dest_token.contract_address,
            "dst_chain": dest_token.chain.name,
            "src_amount": src_amount,
            "src_asset_address": src_token.contract_address,
            "src_chain": src_token.chain.name,
            "wallet_address": wallet,
        }

        response = self.session.post(
            MachClient.quotes,
            json=data,
        )

        return self._handle_response(response, lambda r: Quote(dict(r.json())))  # type: ignore

    def submit_order(self, chain: str, place_taker_tx: str) -> dict:
        data = {
            "chain": chain,
            "place_taker_tx": place_taker_tx,
        }

        response = self.session.post(
            MachClient.orders,
            json=data,
        )

        return self._handle_response(response)

    def get_token_balances(self, wallet_address: str) -> dict[str, dict[str, int]]:
        params = {"wallet_address": wallet_address}

        response = self.session.get(MachClient.token_balances, params=params)

        full_balances = self._handle_response(response)["balances"]

        return {key: value for key, value in full_balances.items() if key in self.chains}


# Singleton
client = MachClient()
