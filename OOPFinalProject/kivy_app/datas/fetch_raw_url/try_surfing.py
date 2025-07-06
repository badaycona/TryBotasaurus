from botasaurus.browser import browser, Driver
from botasaurus.window_size import WindowSize
import time
import os
import re

OUTPUT_DIR = "html_pages" # Tên thư mục để lưu các file HTML
PRODUCT_LINKS = (
    # [f"https://pcpartpicker.com/products/cpu/#page={i}" for i in range(1, 100)] +
    # [f"https://pcpartpicker.com/products/motherboard/#page={j}" for j in range(1, 100)] +
    # [f"https://pcpartpicker.com/products/video-card/#page={i}" for i in range(1, 100)] +
    # [f"https://pcpartpicker.com/products/power-supply/#page={i}" for i in range(1, 100)] +
    [f"https://pcpartpicker.com/products/memory/#page={i}" for i in range(101, 136)]
)

@browser(
    headless=False,
    block_images_and_css=True,
    reuse_driver=True,
    parallel=5,
    cache = True
)
def download_html_pages(driver: Driver, link):
    """
    Đi qua tất cả các trang và lưu mã nguồn HTML của mỗi trang vào một file.
    """
    category = re.search(r'/products/([^/]+)/', link).group(1)  # 'cpu'

    numbers = re.search(r'#page=(\d+)', link)
    numbers = int(numbers.group(1)) if numbers else None
    print(category, numbers)
    driver.google_get(link, bypass_cloudflare=True)
    
    
    try:
        print("Wait for javascript.")
        driver.wait_for_element("tr.tr__product", wait=20)
        print("Loaded succesfully")
    except Exception as e:
        print(f"Not Found")

    html_content = driver.page_html
    file_path = os.path.join(OUTPUT_DIR, f"page_{category}_{numbers}.html")
    
    # Lưu nội dung vào file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Downloaded: {file_path}")
    

if __name__ == "__main__":
    download_html_pages(PRODUCT_LINKS)