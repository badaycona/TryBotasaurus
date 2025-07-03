import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from urllib.parse import urljoin
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class CybeneticsPSUScraper:
    def __init__(self, use_selenium=True):
        self.base_url = "https://www.cybenetics.com"
        self.database_url = "https://www.cybenetics.com/index.php?option=psu-performance-database"
        self.use_selenium = use_selenium
        
        if use_selenium:
            self.setup_selenium()
        else:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
    
    def setup_selenium(self):
        """Cài đặt Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Chạy không hiện giao diện
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("Đã khởi tạo Chrome WebDriver thành công")
        except Exception as e:
            print(f"Lỗi khởi tạo WebDriver: {e}")
            print("Vui lòng cài đặt ChromeDriver hoặc sử dụng requests thay thế")
            self.use_selenium = False
    
    def get_page_content_selenium(self, url):
        """Lấy nội dung trang web bằng Selenium"""
        try:
            self.driver.get(url)
            
            # Đợi trang load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Đợi thêm để JavaScript load xong
            time.sleep(5)
            
            # Tìm các element có thể chứa dữ liệu PSU
            print("Đang tìm kiếm các element chứa dữ liệu...")
            
            # Kiểm tra các selector khả dĩ
            possible_selectors = [
                'table',
                '.table',
                '#psu-table',
                '.psu-list',
                '.database-table',
                '[class*="table"]',
                '[class*="grid"]',
                '[class*="list"]',
                'div[data-table]',
                '.data-table'
            ]
            
            elements_found = {}
            for selector in possible_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        elements_found[selector] = len(elements)
                        print(f"Tìm thấy {len(elements)} element với selector: {selector}")
                except:
                    continue
            
            # In ra HTML của một phần trang để debug
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                html_snippet = body.get_attribute('innerHTML')[:2000]  # Lấy 2000 ký tự đầu
                print("\n--- HTML snippet ---")
                print(html_snippet)
                print("--- End snippet ---\n")
            except:
                pass
            
            return self.driver.page_source
            
        except TimeoutException:
            print("Timeout khi load trang")
            return None
        except Exception as e:
            print(f"Lỗi khi sử dụng Selenium: {e}")
            return None
    
    def get_page_content_requests(self, url, params=None):
        """Lấy nội dung trang web bằng requests"""
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Lỗi khi truy cập {url}: {e}")
            return None
    
    def analyze_page_structure(self, html_content):
        """Phân tích cấu trúc trang để tìm dữ liệu PSU"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("=== PHÂN TÍCH CẤU TRÚC TRANG ===")
        
        # Tìm tất cả các table
        tables = soup.find_all('table')
        print(f"Số lượng table tìm thấy: {len(tables)}")
        
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            rows = table.find_all('tr')
            print(f"  - Số dòng: {len(rows)}")
            if rows:
                first_row = rows[0]
                cells = first_row.find_all(['th', 'td'])
                print(f"  - Số cột: {len(cells)}")
                if cells:
                    headers = [cell.get_text(strip=True)[:50] for cell in cells[:5]]  # Lấy 5 cột đầu
                    print(f"  - Headers mẫu: {headers}")
        
        # Tìm các div có thể chứa dữ liệu
        divs_with_class = soup.find_all('div', class_=True)
        class_names = {}
        for div in divs_with_class:
            for class_name in div.get('class', []):
                if any(keyword in class_name.lower() for keyword in ['table', 'grid', 'list', 'data', 'psu']):
                    class_names[class_name] = class_names.get(class_name, 0) + 1
        
        if class_names:
            print(f"\nCác class có thể chứa dữ liệu: {class_names}")
        
        # Tìm các element có id liên quan
        elements_with_id = soup.find_all(attrs={'id': True})
        relevant_ids = []
        for element in elements_with_id:
            element_id = element.get('id', '')
            if any(keyword in element_id.lower() for keyword in ['table', 'grid', 'list', 'data', 'psu']):
                relevant_ids.append(element_id)
        
        if relevant_ids:
            print(f"Các ID có thể chứa dữ liệu: {relevant_ids}")
        
        # Tìm script tags có thể chứa dữ liệu JSON
        scripts = soup.find_all('script')
        print(f"\nSố script tags: {len(scripts)}")
        for i, script in enumerate(scripts):
            if script.string and any(keyword in script.string.lower() for keyword in ['psu', 'data', 'json']):
                print(f"Script {i+1} có thể chứa dữ liệu PSU")
    
    def extract_psu_data_advanced(self, html_content):
        """Trích xuất dữ liệu PSU với nhiều phương pháp khác nhau"""
        soup = BeautifulSoup(html_content, 'html.parser')
        psu_data = []
        
        # Phương pháp 1: Tìm trong script tags (JSON data)
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Tìm JSON data trong script
                json_matches = re.findall(r'(\[.*?\]|\{.*?\})', script.string, re.DOTALL)
                for match in json_matches:
                    try:
                        data = json.loads(match)
                        if isinstance(data, list) and len(data) > 0:
                            # Kiểm tra xem có phải dữ liệu PSU không
                            first_item = data[0]
                            if isinstance(first_item, dict):
                                keys = list(first_item.keys())
                                if any(keyword in str(keys).lower() for keyword in ['psu', 'model', 'efficiency', 'power']):
                                    print(f"Tìm thấy dữ liệu JSON trong script: {len(data)} items")
                                    return data
                    except:
                        continue
        
        # Phương pháp 2: Tìm trong các table
        tables = soup.find_all('table')
        for table in tables:
            table_data = self.parse_table(table)
            if table_data:
                psu_data.extend(table_data)
        
        # Phương pháp 3: Tìm trong các div có cấu trúc giống grid
        grid_divs = soup.find_all('div', class_=re.compile(r'grid|table|list', re.I))
        for div in grid_divs:
            div_data = self.parse_div_grid(div)
            if div_data:
                psu_data.extend(div_data)
        
        return psu_data
    
    def parse_table(self, table):
        """Parse dữ liệu từ table HTML"""
        rows = table.find_all('tr')
        if len(rows) < 2:  # Cần ít nhất header và 1 dòng dữ liệu
            return []
        
        # Lấy headers
        header_row = rows[0]
        headers = []
        for cell in header_row.find_all(['th', 'td']):
            headers.append(cell.get_text(strip=True))
        
        if not headers:
            return []
        
        # Lấy dữ liệu
        data = []
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) == 0:
                continue
                
            row_data = {}
            for i, cell in enumerate(cells):
                header = headers[i] if i < len(headers) else f"Column_{i}"
                text = cell.get_text(strip=True)
                
                # Tìm links
                links = cell.find_all('a')
                if links:
                    row_data[f"{header}_links"] = [urljoin(self.base_url, link.get('href', '')) for link in links if link.get('href')]
                
                row_data[header] = text
            
            if any(row_data.values()):  # Chỉ thêm nếu có dữ liệu
                data.append(row_data)
        
        return data
    
    def parse_div_grid(self, div):
        """Parse dữ liệu từ div có cấu trúc grid"""
        # Tìm các element con có thể chứa dữ liệu PSU
        items = div.find_all(['div', 'span', 'p'], class_=re.compile(r'item|row|card', re.I))
        if not items:
            return []
        
        data = []
        for item in items:
            item_data = {}
            text = item.get_text(strip=True)
            if text and len(text) > 10:  # Bỏ qua text quá ngắn
                item_data['content'] = text
                
                # Tìm links
                links = item.find_all('a')
                if links:
                    item_data['links'] = [urljoin(self.base_url, link.get('href', '')) for link in links if link.get('href')]
                
                data.append(item_data)
        
        return data
    
    def scrape_psu_database(self):
        """Scrape dữ liệu PSU database"""
        print("Bắt đầu scrape dữ liệu PSU...")
        
        # Lấy nội dung trang
        if self.use_selenium:
            html_content = self.get_page_content_selenium(self.database_url)
        else:
            html_content = self.get_page_content_requests(self.database_url)
        
        if not html_content:
            print("Không thể lấy nội dung trang")
            return []
        
        # Phân tích cấu trúc trang
        self.analyze_page_structure(html_content)
        
        # Trích xuất dữ liệu
        psu_data = self.extract_psu_data_advanced(html_content)
        
        return psu_data
    
    def save_data(self, data, filename_prefix="cybenetics_psu_data"):
        """Lưu dữ liệu ra file"""
        if not data:
            print("Không có dữ liệu để lưu")
            return None, None
        
        # Tạo thư mục output nếu chưa có
        os.makedirs('output', exist_ok=True)
        
        # Lưu ra JSON trước
        json_file = f"output/{filename_prefix}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu dữ liệu ra file JSON: {json_file}")
        
        # Lưu ra CSV nếu có thể
        try:
            df = pd.DataFrame(data)
            csv_file = f"output/{filename_prefix}.csv"
            df.to_csv(csv_file, index=False, encoding='utf-8')
            print(f"Đã lưu {len(data)} PSU ra file CSV: {csv_file}")
            return csv_file, json_file
        except Exception as e:
            print(f"Không thể lưu CSV: {e}")
            return None, json_file
    
    def close(self):
        """Đóng WebDriver nếu đang sử dụng"""
        if self.use_selenium and hasattr(self, 'driver'):
            self.driver.quit()

def main():
    """Hàm main để chạy scraper"""
    print("=== CYBENETICS PSU SCRAPER ===")
    print("Chọn phương pháp scraping:")
    print("1. Sử dụng Selenium (khuyến nghị, xử lý được JavaScript)")
    print("2. Sử dụng requests (nhanh hơn nhưng không xử lý JavaScript)")
    
    choice = input("Nhập lựa chọn (1 hoặc 2): ").strip()
    use_selenium = choice == "1"
    
    if use_selenium:
        print("\nLưu ý: Cần cài đặt ChromeDriver để sử dụng Selenium")
        print("Tải ChromeDriver tại: https://chromedriver.chromium.org/")
    
    scraper = CybeneticsPSUScraper(use_selenium=use_selenium)
    
    try:
        # Scrape dữ liệu
        psu_data = scraper.scrape_psu_database()
        
        if psu_data:
            print(f"\n✅ Đã scrape thành công {len(psu_data)} items")
            
            # Hiển thị mẫu dữ liệu
            print("\n--- MẪU DỮ LIỆU ---")
            for i, item in enumerate(psu_data[:3]):
                print(f"\nItem {i+1}:")
                for key, value in item.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
            
            # Lưu dữ liệu
            csv_file, json_file = scraper.save_data(psu_data)
            
            print(f"\n📊 THỐNG KÊ:")
            print(f"- Tổng số items: {len(psu_data)}")
            print(f"- File JSON: {json_file}")
            if csv_file:
                print(f"- File CSV: {csv_file}")
            
        else:
            print("❌ Không scrape được dữ liệu nào")
            print("Có thể trang web sử dụng JavaScript hoặc có cấu trúc phức tạp")
            print("Hãy thử sử dụng Selenium hoặc kiểm tra lại URL")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()