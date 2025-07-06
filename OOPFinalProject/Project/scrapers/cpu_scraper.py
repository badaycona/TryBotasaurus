# scrapers/cpu_scraper.py
from botasaurus.browser import browser, Driver
from bs4 import BeautifulSoup
from .base_scraper import scrape_all_pages

def extract_cpu_data(soup: BeautifulSoup):
    products = []
    rows = soup.select('tr.tr__product')

    for row in rows:
        name_element = row.select_one('td.td__name .td__nameWrapper p a')
        price_element = row.select_one('td.td__price a')

        products.append({
            'name': name_element.get_text(strip=True) if name_element else 'N/A',
            'core_count': row.select_one('td.td__spec--1').get_text(strip=True),
            'performance_core_clock': row.select_one('td.td__spec--2').get_text(strip=True),
            'integrated_graphics': row.select_one('td.td__spec--5').get_text(strip=True),
            'price': price_element.get_text(strip=True) if price_element else 'N/A'
        })
    return products

@browser(
    cache=True, 
    block_images_and_css=True,
    output="cpus" 
)
def scrape_cpus(driver: Driver, data):
    url = "https://pcpartpicker.com/products/cpu/"
    print(f"Bắt đầu cào dữ liệu CPU từ: {url}")
    
    driver.get(url, bypass_cloudflare=True)
    
    cpu_data = scrape_all_pages(driver, extract_cpu_data)
    
    print(f"Hoàn tất. Đã cào được {len(cpu_data)} sản phẩm CPU.")
    return cpu_data