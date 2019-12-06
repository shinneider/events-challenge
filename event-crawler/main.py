import asyncio
from app.shared.logger import Logger
from app.sympla.crawler import run_sympla_crawler


async def main():
    Logger.info('starting crawler')
    await run_sympla_crawler()
    Logger.info('crawler finished')

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())