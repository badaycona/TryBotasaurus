from utils.cloudflare_bypass import get_bypassed_page_source
from utils.json_writer import save_json
from utils.logger import get_logger
from bs4 import BeautifulSoup

logger = get_logger('cpu_scraper')

def parse_cpus(html):
    soup = BeautifulSoup(html, 'lxml')
    cpus = []
    table = soup.find('table', {'id': 'category_table'})
    if not table:
        logger.error('Could not find CPU table')
        return cpus
    for row in table.select('tbody tr'):
        name_tag = row.select_one('td[class*="td__name"] a')
        price_tag = row.select_one('td[class*="td__price"]')
        if name_tag:
            name = name_tag.get_text(strip=True)
            link = 'https://pcpartpicker.com' + name_tag['href']
        else:
            name = link = None
        price = price_tag.get_text(strip=True) if price_tag else None
        cpus.append({
            'name': name,
            'link': link,
            'price': price
        })
    return cpus

async def scrape_cpus():
    url = 'https://pcpartpicker.com/products/cpu/'
    html = get_bypassed_page_source(url)
    cpus = parse_cpus(html)
    save_json('cpus.json', cpus)
    logger.info(f'Scraped {len(cpus)} CPUs')
