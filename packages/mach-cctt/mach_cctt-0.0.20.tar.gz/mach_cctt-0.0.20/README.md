# Cross Chain Trade Test (CCTT)

Test automated trades between multiple chains on Mach.

## Overview

Test automated trades on Mach. Specify a start chain and symbol, and a policy determining how the destination token will be chosen (randomize chain and symbol, randomize chain and fix symbol). In each trade, the test wallet's entire balance of the source token will be sold for the destination token, and then the destination token because the new source token for the next trade. This continues until the script is killed by the user.

## Usage

1. Install

    ```bash
    python -m pip install mach-cctt
    ```

1. Usage

    ```bash
    cctt --help
    ```

1. Example

    ```bash
    # The script will create log files and an account data file. Make a working directory for it.
    mkdir cctt/ && cd cctt/
    
    cctt import --password abc <private-key> # Import account
    cctt decrypt --password abc # Show public/private key
    cctt balances # Show account balances

    # Trade USDC on random chains, starting from optimism-USDC
    cctt run --password abc --source optimism-USDC --destination-policy fixed:USDC

    # Trade between random tokens on random chains, starting from arbitrum-USDT
    cctt run --password abc --source arbitrum-USDT --destination-policy random
    
    # If the --source is empty, then an appropriate source with a non-zero balance is chosen for you.
    cctt run --password abc --source --destination-policy random
    ```

    Notes:
    
    - You need to have a gas on every chain, or a gas of exactly 0 on chains that you do not wish the testing script to trade on, which will cause those chains to be disabled.
    - The `--source` token should be one that you hold a non-zero balance of in your wallet. If you set it to empty, it will be automatically chosen as any token with a non-zero balance in the wallet.
    - There is a known issue with trades filling for a single tick less than the order was placed at. As a preventative measure, any token balance of 1 tick in the wallet is treated as an empty balance.

## Development

### Requirements

You need the [`just`](https://github.com/casey/just) command runner and either Python 3.12.5+ with `virtualenv`, or `pyenv`.

### Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/tristeroresearch/cross-chain-trade-test.git
    cd cross-chain-trade-test
    ```

1. **Create and activate a virtual environment**

    Using `venv`:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    Or using `pyenv`:

    ```bash
    pyenv virtualenv 3.12.5 cctt
    pyenv activate
    ```

1. **Install dependencies**

    ```bash
    just init
    ```

1. **View available recipes**

    ```bash
    just -l
    ```

    Note that there are recipes that allow you to run the application in-source without needed to build and package to PyPI first:

    ```bash
    just account_file=account.json import <private key> # Import a new account
    just decrypt # Show public and private key
    just balances # List balances of account
    just source=arbitrum-USDC policy=random run # Run the trade tester, starting from arbitrum-USDC and trading to random tokens
    just wallet=<public key> withdraw # Withdraw funds from the stored account to the given wallet
    ```

1. **Building**

    ```bash
    just build
    ```

#### Packaging

Make sure to bump the version number in `pyproject.toml`.

To upload to the test PyPI:

```bash
just upload-test
```

To upload to the main PyPI:

```bash
just upload
```

## TODO

- `drain_eth` is being skipped during withdrawals as we aren't calculating L1 gas fees, making it impossible to determine the amount to withdraw
- Use type 2 (EIP 1559) txs
- Resolve duplication between transfers.py and transactions.py
- Use Quote class from backend and deserialize with pydantic
- Unit tests
