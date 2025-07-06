from utils.cloudflare_bypass import get_bypassed_page_source
from utils.json_writer import save_json
from utils.logger import get_logger
from bs4 import BeautifulSoup

logger = get_logger('gpu_scraper')

def parse_gpus(html):
    soup = BeautifulSoup(html, 'lxml')
    gpus = []
    table = soup.find('table', {'id': 'category_table'})
    if not table:
        logger.error('Could not find GPU table')
        return gpus
    for row in table.select('tbody tr'):  # Each GPU row
        name_tag = row.select_one('td[class*="td__name"] a')
        price_tag = row.select_one('td[class*="td__price"]')
        if name_tag:
            name = name_tag.get_text(strip=True)
            link = 'https://pcpartpicker.com' + name_tag['href']
        else:
            name = link = None
        price = price_tag.get_text(strip=True) if price_tag else None
        gpus.append({
            'name': name,
            'link': link,
            'price': price
        })
    return gpus

async def scrape_gpus():
    url = 'https://pcpartpicker.com/products/video-card/'
    html = get_bypassed_page_source(url)
    gpus = parse_gpus(html)
    save_json('gpus.json', gpus)
    logger.info(f'Scraped {len(gpus)} GPUs')
