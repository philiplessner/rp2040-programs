import asyncio
import aiohttp
from aiohttp import ClientSession
from common import async_timed, fetch_status


@async_timed()
async def main():
    async with ClientSession() as session:
        urls = ['http://192.168.1.66' for _ in range(10)]
        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results
                              if not isinstance(res, Exception)]
        print(f"All Results: {results}")
        print(f"Finished Successfully: {successful_results}")
        print(f"Threw Exceptions: {exceptions}")


if __name__ == "__main__":
    asyncio.run(main())
