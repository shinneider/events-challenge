import inspect
import asyncio
from pyppeteer import launch
from config import settings
from bs4 import BeautifulSoup
from app.shared.logger import Logger


class EventsListCrawler:
    """
        This crawlers get all events urls for event page
    """
    MAX_PAGE = 1  # use -1 to get all pages,
    PAGINATOR = '?ordem=data&pagina={page}'

    def __init__(self, *args, **kwargs):
        self.browser = launch(
            headless=settings.BROWSER_HEADLESS,
            executablePath="/usr/bin/chromium-browser",
            args= ['--no-sandbox', "--disable-gpu", "--disable-software-rasterizer", "--disable-dev-shm-usage"]
        )

    async def start_crawler(self):
        if inspect.isawaitable(self.browser):
            self.browser = await self.browser

        page = await self.browser.newPage()
        await page.setUserAgent(settings.USER_AGENT_STRING)
        
        event_url = []

        loaded_page = 0 
        erros = 0
        while loaded_page != self.MAX_PAGE:
            try:  # prevent not load page if error
                Logger.info(f" |--> Getting page: {loaded_page}")
                await self.get_page(page, loaded_page)
                content = await self.get_body_data(page)
                event_url += await self.get_event_url(content)
                loaded_page += 1
                erros = 0
                Logger.info(f" |     '-> success")
            except Exception as e:
                Logger.error(f" |     '-> error {e}")
                # if 3 or more erro in same page, jump to the next
                erros += 1
                if erros > 3:
                    loaded_page + 1
        
        return event_url
            
    async def get_page(self, page, page_number):
        url = settings.SYMPLA_EVENTS_URL
        url += self.PAGINATOR.format(page=page_number)
        await page.goto(url, timeout=(60 * 1000), waitUntil='domcontentloaded')

    async def get_body_data(self, page):
        return await page.evaluate('document.body.innerHTML')

    async def get_event_url(self, raw):
        soup = BeautifulSoup(raw, "html.parser")

        urls = []
        for element in soup.find_all('a', {'class' : 
                            'sympla-card w-inline-block'}, limit=None):
            urls.append(element['href'])

        return urls
