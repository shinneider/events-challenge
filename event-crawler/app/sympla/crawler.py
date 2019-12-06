from app.sympla.crawler_events_list import EventsListCrawler
from app.sympla.crawler_event_page import EventsPageCrawler
from app.shared.logger import Logger
from app.shared.utils import site_data
from config import settings


async def run_sympla_crawler():
    Logger.info('Crawling page for events urls')
    events_urls = await EventsListCrawler().start_crawler()
    Logger.info(" '-> Finished\n")

    Logger.info('Crawling all events urls')
    events = await EventsPageCrawler().start_crawler(events_urls)
    Logger.info(" '-> Finished\n")
    
    Logger.info('Sending data to events micro-service')
    site_data(url=settings.MICRO_SERVICE_EVENT_URL, method='POST', 
              expected_status=201, output='text', json=events)
    Logger.info(" '-> Finished\n")