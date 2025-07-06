# --- START OF FILE retriever.py (phiên bản cuối cùng, đáng tin cậy) ---

import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import json
import os
from requests_html import HTMLSession, HTML
class HybridRetriever:
    def __init__(self, cookie_file='cookies.json'):
        self.cookie_file = cookie_file
        self.session = HTMLSession() # Sử dụng HTMLSession thay vì requests.Session
        
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        self.session.headers.update({'User-Agent': self.user_agent})
        
        self._load_cookies()

    def _load_cookies(self):
        """Tải cookie từ file JSON và nạp vào session."""
        if not os.path.exists(self.cookie_file):
            raise FileNotFoundError(f"Không tìm thấy file cookie '{self.cookie_file}'.")
        
        print(f"Đang tải cookie từ '{self.cookie_file}'...")
        with open(self.cookie_file, 'r') as f:
            cookies = json.load(f)
            
        for cookie in cookies:
            self.session.cookies.set(
                name=cookie['name'], value=cookie['value'],
                domain=cookie['domain'], path=cookie.get('path', '/')
            )
        print("Tải cookie thành công!")

    def get_response(self, url: str) -> requests.Response:
        """
        Sử dụng session với cookie để lấy HTML, sau đó render JavaScript.
        """
        print(f"Đang lấy dữ liệu từ: {url}")
        
        # Bước 1: Dùng session để lấy HTML ban đầu
        response = self.session.get(url)
        
        if "Just a moment..." in response.text or "challenge-platform" in response.text:
             raise Exception("Bị Cloudflare chặn! Cookie có thể đã hết hạn hoặc không hợp lệ.")
        
        response.raise_for_status()

        # Bước 2: Thực thi JavaScript trên HTML đã nhận được
        # Đây là bước "chờ đợi" mà bạn muốn!
        print("HTML ban đầu đã được tải. Đang thực thi JavaScript để tải dữ liệu...")
        try:
            # scrolldown: cuộn trang xuống để kích hoạt tải dữ liệu (nếu cần)
            # sleep: chờ một vài giây để đảm bảo JS chạy xong
            # timeout: thời gian tối đa để render
            response.html.render(scrolldown=1, sleep=3, timeout=30)
            print("JavaScript đã thực thi xong.")
        except Exception as e:
            print(f"Lỗi trong quá trình render JavaScript: {e}")
            # Dù có lỗi, chúng ta vẫn có thể thử phân tích nội dung đã có
            
        # Trả về đối tượng response đã được cập nhật
        return response
class CookieRetriever:
    def __init__(self, cookie_file='cookies.json'):
        self.cookie_file = cookie_file
        self.session = requests.Session()
        
        # Đặt một User-Agent trông giống thật
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        })
        
        self._load_cookies()

    def _load_cookies(self):
        """Tải cookie từ file JSON và nạp vào session."""
        if not os.path.exists(self.cookie_file):
            raise FileNotFoundError(
                f"Không tìm thấy file cookie '{self.cookie_file}'.\n"
                f"Vui lòng làm theo hướng dẫn để xuất cookie từ trình duyệt của bạn."
            )
            
        print(f"Đang tải cookie từ '{self.cookie_file}'...")
        with open(self.cookie_file, 'r') as f:
            cookies = json.load(f)
            
        for cookie in cookies:
            # requests chỉ cần các trường cơ bản này
            self.session.cookies.set(
                name=cookie['name'],
                value=cookie['value'],
                domain=cookie['domain'],
                path=cookie.get('path', '/')
            )
        print("Tải cookie thành công!")

    def get_response(self, url: str) -> requests.Response:
        """Sử dụng session đã có cookie để gửi yêu cầu."""
        print(f"Đang lấy dữ liệu từ: {url}")
        try:
            response = self.session.get(url)
            # Kiểm tra xem cookie có còn hợp lệ không
            if "Just a moment..." in response.text or "challenge-platform" in response.text:
                 raise Exception(
                     "Bị Cloudflare chặn! Cookie có thể đã hết hạn hoặc không hợp lệ.\n"
                     "Vui lòng xuất lại cookie mới từ trình duyệt."
                 )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gửi yêu cầu: {e}")
            raise
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
class SeleniumScrapingRetriever:
    def __init__(self):
        print("Đang cấu hình trình duyệt Chrome với stealth...")
        
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Lỗi khởi tạo webdriver: {e}")
            raise

        stealth(self.driver,
                languages=["en-US", "en"], vendor="Google Inc.", platform="Win32",
                webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        self.is_ready = False
        print("Trình duyệt đã sẵn sàng.")

    def initial_setup(self, test_url="https://pcpartpicker.com/"):
        print(f"\nĐang mở trang: {test_url}")
        print("="*50)
        print("VUI LÒNG CHÚ Ý:")
        print("1. Một cửa sổ trình duyệt Chrome sẽ mở ra.")
        print("2. Nếu trang web yêu cầu bạn xác minh (ví dụ: giải CAPTCHA), hãy hoàn thành nó.")
        print("3. Sau khi trang web tải xong hoàn toàn, hãy quay lại cửa sổ console này và nhấn ENTER.")
        print("4. **KHÔNG ĐÓNG** cửa sổ trình duyệt này. Nó sẽ được sử dụng cho toàn bộ quá trình scraping.")
        print("="*50)
        
        self.driver.get(test_url)
        input("Nhấn ENTER sau khi bạn đã giải CAPTCHA và trang đã tải xong...")
        self.is_ready = True
        print("\nThiết lập hoàn tất! Trình duyệt sẽ được giữ mở để scraping.")

    def get_response(self, url: str) -> requests.Response:
        """
        Sử dụng Selenium để truy cập URL, đợi JS tải xong, và trả về nội dung.
        """
        if not self.is_ready:
            raise Exception("Bạn phải chạy `initial_setup()` trước khi gọi `get_response()`.")
        
        print(f"Selenium đang điều hướng đến: {url}")
        self.driver.get(url)
        
        try:
            # Đợi cho đến khi bảng dữ liệu xuất hiện (tối đa 20 giây)
            # Đây là yếu tố then chốt!
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "paginated_table"))
            )
            print("Bảng dữ liệu đã được tải.")
        except Exception:
            print(f"Không tìm thấy bảng dữ liệu tại {url} sau khi chờ.")
            # Kiểm tra xem có phải bị chặn không
            if "Just a moment..." in self.driver.page_source or "challenge-platform" in self.driver.page_source:
                 raise Exception("Bị Cloudflare chặn! Hãy thử chạy lại chương trình.")

        # Tạo một đối tượng Response giả để tương thích với code scraper hiện tại
        response = requests.Response()
        response.status_code = 200
        response.url = self.driver.current_url
        # Gán nội dung trang SAU KHI JS đã chạy vào đối tượng response
        response._content = self.driver.page_source.encode('utf-8')
        
        return response

    def close(self):
        """Đóng trình duyệt khi scraping xong."""
        if self.driver:
            print("Đang đóng trình duyệt...")
            self.driver.quit()