import asyncio
from pyppeteer import launch
from app.sympla.crawler_events import EventsListCrawler


async def main():
    await EventsListCrawler().start_crawler()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())