# --- START OF FILE retriever.py (phiên bản cuối cùng, đáng tin cậy) ---

import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

class SeleniumRetriever:
    def __init__(self):
        print("Đang cấu hình trình duyệt Chrome với stealth...")
        
        # Cấu hình các tùy chọn cho Chrome theo cú pháp mới và đúng
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # Dòng này sử dụng cú pháp đúng để loại bỏ các dấu hiệu tự động hóa
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        print("Sử dụng webdriver-manager để tự động tải/quản lý ChromeDriver...")
        try:
            # Tự động tải driver tương thích với phiên bản Chrome của bạn (ví dụ: 131)
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Lỗi nghiêm trọng khi khởi tạo webdriver: {e}")
            print("Hãy chắc chắn rằng bạn có kết nối mạng và Chrome đã được cài đặt đúng cách.")
            raise

        # Áp dụng các kỹ thuật "tàng hình"
        print("Áp dụng các lớp bảo vệ stealth...")
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        self.session = requests.Session()
        self.is_ready = False
        print("Trình duyệt đã sẵn sàng.")

    def initial_setup(self, test_url="https://pcpartpicker.com/"):
        print(f"\nĐang mở trang: {test_url}")
        print("="*50)
        print("VUI LÒNG CHÚ Ý:")
        print("1. Một cửa sổ trình duyệt Chrome sẽ mở ra.")
        print("2. Nếu trang web yêu cầu bạn xác minh (ví dụ: giải CAPTCHA), hãy hoàn thành nó.")
        print("3. Sau khi trang web tải xong hoàn toàn, hãy quay lại cửa sổ console này và nhấn ENTER.")
        print("="*50)
        
        self.driver.get(test_url)
        
        input("Nhấn ENTER sau khi bạn đã giải CAPTCHA và trang đã tải xong...")
        
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

        user_agent = self.driver.execute_script("return navigator.userAgent;")
        self.session.headers.update({"User-Agent": user_agent})
        
        self.is_ready = True
        print("\nThiết lập hoàn tất! Cookie đã được lưu. Bây giờ các yêu cầu sẽ được thực hiện dưới nền.")
        self.driver.quit()

    def get_response(self, url: str) -> requests.Response:
        if not self.is_ready:
            raise Exception("Bạn phải chạy `initial_setup()` trước khi gọi `get_response()`.")
        
        print(f"Đang lấy dữ liệu từ: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            if e.response.status_code == 403:
                print("Lỗi 403! Cookie có thể đã hết hạn. Hãy thử chạy lại chương trình.")
            raise

    def __del__(self):
        # Đảm bảo trình duyệt luôn được đóng
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
            except:
                pass