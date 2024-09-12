from abc import ABC, abstractmethod
from collections import defaultdict
from typing import AbstractSet

from .client import client
from . import config
from .data_types import Chain, Token
from .utility import random_set_choice


class DestinationPolicy(ABC):
    def __init__(
        self, initial_excluded_chains: AbstractSet[str] = config.excluded_chains
    ):
        self.token_choices = defaultdict(
            set,
            {
                chain: set(chain_info["assets"].keys()) - frozenset((client.gas_tokens[chain], ))
                for chain, chain_info in client.deployments.items()
                if chain not in initial_excluded_chains
            },
        )

        self.tried_tokens: list[Token] = []

    # Permanently exclude a chain
    def exclude_chain(self, chain: Chain) -> None:
        del self.token_choices[chain.name]

    # Temporarily exclude a chain from the current trade
    def add_tried_chain(self, chain: Chain) -> None:
        self.tried_chain = (chain.name, self.token_choices[chain.name])
        del self.token_choices[chain.name]

    # Temporarily exclude a token from the current trade
    def add_tried_token(self, token: Token) -> None:
        self.token_choices[token.chain.name].remove(token.symbol)

        # Remove this chain if there are no tokens we can choose from it
        if not self.token_choices[token.chain.name]:
            del self.token_choices[token.chain.name]

        self.tried_tokens.append(token)

    # Reset for the next trade
    def reset(self) -> None:
        if self.tried_chain:
            self.token_choices[self.tried_chain[0]] = self.tried_chain[1]
            self.tried_chain = None  # type: ignore

        for token in self.tried_tokens:
            self.token_choices[token.chain.name].add(token.symbol)

        self.tried_tokens.clear()

    # Produce the destination token for the next trade
    @abstractmethod
    def __call__(self) -> Token: ...


class RandomChainFixedSymbolPolicy(DestinationPolicy):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def __call__(self) -> Token:
        try:
            chain = random_set_choice(self.token_choices.keys())
        except IndexError as e:
            raise RuntimeError(
                "Unable to choose destination token - all choices have been excluded"
            ) from e

        return Token.from_components(chain, self.symbol)


class RandomChainRandomSymbolpolicy(DestinationPolicy):
    def __init__(self):
        super().__init__()

    def __call__(self) -> Token:
        try:
            chain = random_set_choice(self.token_choices.keys())
            symbol = random_set_choice(self.token_choices[chain])
        except IndexError as e:
            raise RuntimeError(
                "Unable to choose destination token - all choices have been excluded"
            ) from e

        return Token.from_components(chain, symbol)
