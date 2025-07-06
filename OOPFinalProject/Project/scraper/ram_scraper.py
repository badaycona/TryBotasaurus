from utils.cloudflare_bypass import get_bypassed_page_source
from utils.json_writer import save_json
from utils.logger import get_logger
from bs4 import BeautifulSoup

logger = get_logger('ram_scraper')

def parse_rams(html):
    soup = BeautifulSoup(html, 'lxml')
    rams = []
    table = soup.find('table', {'id': 'category_table'})
    if not table:
        logger.error('Could not find RAM table')
        return rams
    for row in table.select('tbody tr'):
        name_tag = row.select_one('td[class*="td__name"] a')
        price_tag = row.select_one('td[class*="td__price"]')
        if name_tag:
            name = name_tag.get_text(strip=True)
            link = 'https://pcpartpicker.com' + name_tag['href']
        else:
            name = link = None
        price = price_tag.get_text(strip=True) if price_tag else None
        rams.append({
            'name': name,
            'link': link,
            'price': price
        })
    return rams

async def scrape_rams():
    url = 'https://pcpartpicker.com/products/memory/'
    html = get_bypassed_page_source(url)
    rams = parse_rams(html)
    save_json('rams.json', rams)
    logger.info(f'Scraped {len(rams)} RAM modules')
