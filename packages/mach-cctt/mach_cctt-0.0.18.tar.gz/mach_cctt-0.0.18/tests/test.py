import asyncio

from web3 import AsyncWeb3

async def f():
    pass

async def g() -> int:
    raise Exception()

async def main():
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider("https://eth.llamarpc.com"))
    
    await asyncio.gather(
        w3.eth.get_balance("0xF05EeD33a37F0Ab8AbDba2468E23875A58b0f648"),
        f(),
        g()
    )


if __name__ == "__main__":
    asyncio.run(main())
