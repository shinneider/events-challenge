import inspect
import asyncio
from pyppeteer import launch
from config import settings
from bs4 import BeautifulSoup


class EventsPageCrawler:
    """
        This crawlers get all data from event
         - city: string
         - state: string with 2 letters
         - name: string
         - description: string
         - start and finish date: string in format YYYY-MM-DDTHH:MM
         - event-url: url string
         - ticket: list {name, value}
    """
    pass
