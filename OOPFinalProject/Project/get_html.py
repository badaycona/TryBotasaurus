from botasaurus.browser import browser, Driver

TARGET_URL = "https://pcpartpicker.com/products/cpu/"

OUTPUT_FILENAME = "page_source.html"

@browser(
    
    cache=False
)
def fetch_and_save_html(driver: Driver, data):
    url_to_fetch = data['url']
    print(f"Đang truy cập URL: {url_to_fetch}")
    
    driver.get(url_to_fetch, bypass_cloudflare=True)
    
    print("Đang chờ trang tải xong...")
    driver.sleep(5) # Chờ 5 giây

    print("Đang lấy mã nguồn HTML...")
    html_content = driver.page_html
    
    print(f"Lấy HTML thành công! Kích thước: {len(html_content)} bytes.")
    
    return html_content

if __name__ == "__main__":
    page_html = fetch_and_save_html(data={'url': TARGET_URL})
    
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"Đã lưu thành công mã nguồn HTML vào file: '{OUTPUT_FILENAME}'")
        print("Bây giờ bạn có thể mở file này bằng trình duyệt để xem cấu trúc.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lưu file: {e}")