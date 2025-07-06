from bs4 import BeautifulSoup
from botasaurus.task import task
from botasaurus.browser import browser, Driver, NotFoundException
from botasaurus.soupify import soupify

@browser(
    # proxy='http://username:password@datacenter-proxy-domain:proxy-port', # Uncomment to use Proxy ONLY if you face IP blocking

    # block_images_and_css=True, # Uncomment to block images and CSS, which can speed up scraping
    # wait_for_complete_page_load=False, # Uncomment to proceed once the DOM (Document Object Model) is loaded, without waiting for all resources to finish loading. This is recommended for faster scraping of Server Side Rendered (HTML) pages.

    cache=True,
    max_retry=5,  # Retry up to 5 times, which is a good default

    reuse_driver= True, # Reuse the same driver for all tasks
    
    output=None,

    close_on_crash=True,
    raise_exception=True,
    create_error_logs=False,
)
def scrape_html(driver: Driver, link):
    # Scrape the HTML and cache it
    if driver.config.is_new:
        driver.google_get(
            link,
            bypass_cloudflare=True,  # delete this line if the website you're accessing is not protected by Cloudflare
        )
    response = driver.requests.get(link)
    
    if response.status_code == 404:
        # A Special Exception to skip retrying this link
        raise NotFoundException(link)
    response.raise_for_status()
    
    html = response.text        
    return html

def extract_data(soup: BeautifulSoup):
    # Extract the heading from the HTML
    stock_name = soup.select_one('[data-testid="quote-hdr"] h1').get_text()
    stock_price = soup.select_one('[data-testid="qsp-price"]').get_text()
    
    return {
        "stock_name": stock_name,
        "stock_price": stock_price,
    }

# Cache the scrape_data task as well
@task(
    cache=True,
    close_on_crash=True,
    create_error_logs=False,
)
def scrape_data(link):
    # Call the scrape_html function to get the cached HTML
    html = scrape_html(link)
    # Extract data from the HTML using the extract_data function
    return extract_data(soupify(html))

data_items = [
    "https://finance.yahoo.com/quote/AAPL/",
    "https://finance.yahoo.com/quote/GOOG/",
    "https://finance.yahoo.com/quote/MSFT/",
]

scrape_data(data_items)