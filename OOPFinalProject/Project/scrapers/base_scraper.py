# scrapers/base_scraper.py
from botasaurus.browser import Driver
from botasaurus.soupify import soupify
import time

def scrape_all_pages(driver: Driver, extract_function):
    """
    Hàm chung để cào dữ liệu từ tất cả các trang của một danh mục sản phẩm.

    :param driver: Đối tượng Driver của Botasaurus.
    :param extract_function: Một hàm nhận vào một đối tượng BeautifulSoup và trả về một danh sách các sản phẩm từ trang đó.
    """
    all_products = []
    page_number = 1

    while True:
        print(f"Đang cào dữ liệu trang {page_number}...")
        
        print("Đang chờ bảng sản phẩm tải...")
        driver.wait_for_element('#product-list', 15)
        
        soup = soupify(driver)
        products_on_page = extract_function(soup)
        all_products.extend(products_on_page)
        
        print(f"Đã tìm thấy {len(products_on_page)} sản phẩm trên trang {page_number}. Tổng số: {len(all_products)}.")

        next_button = driver.select('li.page-item.next a')

        if next_button and 'disabled' not in next_button.get_attribute('class', ''):
            print("Chuyển sang trang tiếp theo...")
            next_button.click()
            time.sleep(2)
            page_number += 1
        else:
            print("Đã đến trang cuối cùng.")
            break
            
    return all_products