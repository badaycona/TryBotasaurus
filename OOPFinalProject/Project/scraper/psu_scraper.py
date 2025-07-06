from utils.cloudflare_bypass import get_bypassed_page_source
from utils.json_writer import save_json
from utils.logger import get_logger
from bs4 import BeautifulSoup

logger = get_logger('psu_scraper')

def parse_psus(html):
    soup = BeautifulSoup(html, 'lxml')
    psus = []
    table = soup.find('table', {'id': 'category_table'})
    if not table:
        logger.error('Could not find PSU table')
        return psus
    for row in table.select('tbody tr'):
        name_tag = row.select_one('td[class*="td__name"] a')
        price_tag = row.select_one('td[class*="td__price"]')
        if name_tag:
            name = name_tag.get_text(strip=True)
            link = 'https://pcpartpicker.com' + name_tag['href']
        else:
            name = link = None
        price = price_tag.get_text(strip=True) if price_tag else None
        psus.append({
            'name': name,
            'link': link,
            'price': price
        })
    return psus

async def scrape_psus():
    url = 'https://pcpartpicker.com/products/power-supply/'
    html = get_bypassed_page_source(url)
    psus = parse_psus(html)
    save_json('psus.json', psus)
    logger.info(f'Scraped {len(psus)} PSUs')
