from botasaurus.browser import browser, Driver
from lxml import etree

# URL sitemap bạn đang bị chặn 403
SITEMAP_URL = "https://pcpartpicker.com/sitemap.xml" 

@browser(
    # Bật headless=False để bạn có thể nhìn thấy chính xác trình duyệt đang làm gì.
    # Khi đã chạy thành công, bạn có thể đổi thành True để chạy ẩn.
    headless=False,
    
    # Bỏ comment và điền proxy của bạn vào đây nếu nghi ngờ bị chặn IP.
    # Nên dùng proxy dân cư (residential proxy) để có hiệu quả cao nhất.
    # proxy="http://username:password@proxy-provider-domain:port",
    
    # Chặn ảnh và CSS để trang tải nhanh hơn, dù không quá quan trọng với file XML.
    block_images_and_css=True,
)
def get_sitemap_with_browser(driver: Driver, data: dict):
    """
    Sử dụng trình duyệt ảo để truy cập sitemap, vượt qua các biện pháp bảo vệ.
    """
    print("--- BẮT ĐẦU KỊCH BẢN DÙNG TRÌNH DUYỆT ẢO ---")
    
    # Kỹ thuật 1: Giả lập truy cập từ kết quả tìm kiếm của Google.
    # Đây là kỹ thuật chống chặn hiệu quả nhất.
    print(f"Bước 1: Giả lập truy cập '{SITEMAP_URL}' từ Google...")
    driver.google_get(SITEMAP_URL, 
                      # Kỹ thuật 2: Tự động vượt qua các thử thách của Cloudflare.
                      # Nếu trang không dùng Cloudflare, tham số này cũng không gây hại.
                      bypass_cloudflare=True)
                      
    print("Bước 2: Đã truy cập thành công! Trình duyệt đang hiển thị nội dung sitemap.")
    
    # Dừng lại một chút để đảm bảo mọi thứ đã tải xong hoàn toàn.
    driver.short_random_sleep()

    # Kỹ thuật 3: Lấy toàn bộ mã nguồn của trang mà trình duyệt đang hiển thị.
    print("Bước 3: Đang lấy mã nguồn (XML) từ trình duyệt...")
    xml_content_string = driver.page_source
    
    # Kiểm tra xem có lấy được nội dung XML không hay là trang lỗi.
    if "<!DOCTYPE html>" in xml_content_string.lower() or "403 forbidden" in xml_content_string.lower():
        print("\n[LỖI] Trình duyệt không tải được nội dung XML. Có thể bạn vẫn bị chặn.")
        print("Hãy thử dùng một proxy dân cư tốt.")
        driver.prompt("Kiểm tra cửa sổ trình duyệt và nhấn Enter để thoát.")
        return None

    print("Bước 4: Lấy mã nguồn thành công! Bắt đầu phân tích XML...")
    
    # Phân tích XML bằng lxml
    try:
        root = etree.fromstring(xml_content_string.encode('utf-8'))
        locations = root.xpath("//{*}loc")
        extracted_links = [loc.text for loc in locations]
        print("Bước 5: Phân tích XML hoàn tất.")
        return extracted_links
    except Exception as e:
        print(f"[LỖI] Lỗi khi phân tích XML: {e}")
        driver.prompt("Có lỗi khi phân tích, vui lòng kiểm tra nội dung trang. Nhấn Enter để thoát.")
        return None

# --- Phần thực thi ---
if __name__ == "__main__":
    sitemap_links = get_sitemap_with_browser()
    
    print("\n--- KẾT QUẢ CUỐI CÙNG ---")
    if sitemap_links:
        print(f"Thành công mỹ mãn! Đã trích xuất được {len(sitemap_links)} link từ sitemap.")
        print("5 link đầu tiên là:")
        for link in sitemap_links[:5]:
            print(f"- {link}")
    else:
        print("Nhiệm vụ thất bại. Vui lòng xem lại các thông báo lỗi ở trên.")