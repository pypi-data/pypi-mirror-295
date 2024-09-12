from .client import client
from . import config


class Token:
    __slots__ = ("chain", "symbol", "chain_id", "contract_address", "decimals")

    def __init__(self, identifier: str):
        chain, self.symbol = identifier.split("-")
        self.chain = Chain(chain)
        asset_data = self.chain.data["assets"][self.symbol]
        self.contract_address: str = asset_data["address"]
        self.decimals: int = asset_data["decimals"]

    @classmethod
    def from_components(cls, chain: str, symbol: str):
        return cls(f"{chain}-{symbol}")

    def __eq__(self, other) -> bool:
        return self.chain == other.chain and self.symbol == other.symbol

    def __repr__(self) -> str:
        return f"{self.chain}-{self.symbol}"


class Chain:
    __slots__ = ("name", "id", "data", "lz_cid", "rpc_url")

    def __init__(self, name: str):
        self.name = name
        self.data: dict = client.deployments[self.name]
        self.id: int = self.data["chain_id"]  # type: ignore
        self.lz_cid: int = self.data["lz_cid"]  # type: ignore
        self.rpc_url = config.rpc_urls[name]

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return self.name
