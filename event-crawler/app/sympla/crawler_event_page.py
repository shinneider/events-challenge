import inspect
import asyncio
import locale
from re import findall as re_findall
from datetime import datetime
from pyppeteer import launch
from config import settings
from bs4 import BeautifulSoup
from app.shared.logger import Logger


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
    def __init__(self, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')  ## for date format
        self.browser = launch(
            headless=settings.BROWSER_HEADLESS,
            executablePath="/usr/bin/chromium-browser",
            args= ['--no-sandbox', "--disable-gpu", "--disable-software-rasterizer", "--disable-dev-shm-usage"]
        )

    async def start_crawler(self, events_uls):
        if inspect.isawaitable(self.browser):
            self.browser = await self.browser
        
        page = await self.browser.newPage()
        await page.setUserAgent(settings.USER_AGENT_STRING)

        events = []
        for url in events_uls:
            try:  # prevent not load page if error
                Logger.info(f" |--> starting crawling to: {url}")
                await self.get_page(page, url)
                content = await self.get_body_data(page)
                events.append(await self.get_event_data(content, url))
                Logger.info(f" |     '-> success")
            except Exception as e:
                Logger.error(f" |     '-> error {e}")
        
        return events

    async def get_page(self, page, url):
        await page.goto(url, timeout=(60 * 1000), waitUntil='networkidle0')

    async def get_body_data(self, page):
        return await page.evaluate('document.body.innerHTML')

    async def get_event_data(self, raw, url):
        soup = BeautifulSoup(raw, "html.parser")
        
        data = {'event_url': url}
        data['name'] = soup.find('h1').text.strip()
        data.update(await self.get_event_locate(soup))
        data.update(await self.get_start_end_dates(soup))
        data['tickets'] = await self.get_tickets(soup)

        data['description'] = 'ommited because is too large to logger'
        Logger.info(f" |     '-> data: {data}")

        data['description'] = await self.get_description(soup)
        return data

    async def get_event_locate(self, soup):
        locate = soup.find('div', {'class': 'event-info-city'})
        if locate:
            locate = locate.text
        else:
            locate = soup.find('i', {'class': 'fa fa-map-marker'})
            locate = locate.next_sibling.strip()
        
        if locate.strip().upper() != 'EVENTO ONLINE':
            return {
                'city': {
                    'name': locate.split('-')[-1].split(',')[0].strip(),
                    'state': {
                        'initials': locate.split(',')[-1].strip()
                    }
                },
                'event_online': False
            }

        return { 'event_online': True }

    async def get_start_end_dates(self, soup):
        dates = soup.find('div', {'class': 'event-info-calendar'})
        if dates:
            dates = dates.text
        else:
            dates = soup.find('i', {'class': 'fa fa-calendar'})
            dates = dates.next_sibling.strip()
        
        start, end = dates.split('-')[0].strip(), dates.split('-')[1].strip()

        start += '0' if start.endswith('h') else ''
        end += '0' if end.endswith('h') else ''

        if len(end) <= 5:  ## finish in same day (19h30-22h)
            end = '%s, %s' % (start.split(',')[0], end)

        start = datetime.strptime(start, '%d de %B de %Y, %Hh%M')
        end = datetime.strptime(end, '%d de %B de %Y, %Hh%M')

        return {
            'start_at': start.strftime("%Y-%m-%dT%H:%M"),
            'finish_at': end.strftime("%Y-%m-%dT%H:%M")
        }

    async def get_description(self, soup):
        description = soup.find('div', {'id': 'descricao'})
        return str(description)

    async def get_tickets(self, soup):
        ticket_form = soup.find('form', {'id': 'ticket-form'})

        if not ticket_form:
            return []

        ticket_table = soup.find('tbody')
        tickets_tag = ticket_table.find_all('td')
        
        tickets = []
        for ticket in tickets_tag:
            if ticket['class'] == ['opt-panel']: continue
            if not ticket.find_all('span'): continue

            name = ticket.find_all('span')[0].text.strip()
            price = ticket.find_all('br')[0].next_sibling.strip()
            if not price:
                price = ticket.find_all('span')[1].text.strip()

            if price.startswith('R$'):
                price = float(price[3:].replace('.', '').replace(',', '.'))
            elif price.upper() == 'GRÁTIS':
                price = 0.0
            else:
                raise ValueError(f'invalid price format {price}')

            tickets.append({
                'name': name,
                'text': price
            })

        return tickets