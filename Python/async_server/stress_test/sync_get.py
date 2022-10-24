import asyncio
import aiohttp
from aiohttp import ClientSession
from common import async_timed, fetch_status


@async_timed()
async def main():
    async with ClientSession() as session:
        urls = ['http://192.168.1.66' for _ in range(10)]
        status_codes = [await fetch_status(session, url) for url in urls]
        print(status_codes)


if __name__ == "__main__":
    asyncio.run(main())
