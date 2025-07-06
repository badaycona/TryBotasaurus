from utils.cloudflare_bypass import get_bypassed_page_source
from utils.json_writer import save_json
from utils.logger import get_logger
from bs4 import BeautifulSoup

logger = get_logger('motherboard_scraper')

def parse_motherboards(html):
    soup = BeautifulSoup(html, 'lxml')
    motherboards = []
    table = soup.find('table', {'id': 'category_table'})
    if not table:
        logger.error('Could not find Motherboard table')
        return motherboards
    for row in table.select('tbody tr'):
        name_tag = row.select_one('td[class*="td__name"] a')
        price_tag = row.select_one('td[class*="td__price"]')
        if name_tag:
            name = name_tag.get_text(strip=True)
            link = 'https://pcpartpicker.com' + name_tag['href']
        else:
            name = link = None
        price = price_tag.get_text(strip=True) if price_tag else None
        motherboards.append({
            'name': name,
            'link': link,
            'price': price
        })
    return motherboards

async def scrape_motherboards():
    url = 'https://pcpartpicker.com/products/motherboard/'
    html = get_bypassed_page_source(url)
    motherboards = parse_motherboards(html)
    save_json('motherboards.json', motherboards)
    logger.info(f'Scraped {len(motherboards)} motherboards')
