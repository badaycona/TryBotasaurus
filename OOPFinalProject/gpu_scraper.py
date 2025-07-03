import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_nvidia_gpus():
    # URL của trang liệt kê các dòng sản phẩm GeForce
    base_url = "https://www.nvidia.com"
    series_page_url = f"{base_url}/en-us/geforce/graphics-cards/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Fetching series page: {series_page_url}")
    try:
        series_page = requests.get(series_page_url, headers=headers)
        series_page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching series page: {e}")
        return []

    soup = BeautifulSoup(series_page.content, 'html.parser')
    
    all_gpus = []
    
    # Tìm tất cả các liên kết đến từng series (ví dụ: 40 series, 30 series)
    # Cấu trúc selector này có thể thay đổi, cần kiểm tra lại bằng Inspect Element
    series_links = soup.select('a.hf-c-series-grid__item')

    if not series_links:
        print("Could not find series links. The website structure might have changed.")
        return []
        
    for link in series_links:
        series_url = base_url + link['href']
        print(f"\n--- Scraping Series: {series_url} ---")
        
        try:
            page = requests.get(series_url, headers=headers)
            page.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {series_url}: {e}")
            continue

        series_soup = BeautifulSoup(page.content, 'html.parser')
        
        # Tìm các thẻ chứa thông tin từng GPU trong series
        # Selector này cũng rất dễ thay đổi.
        product_cards = series_soup.select('.prod-card')
        
        if not product_cards:
            print(f"No product cards found on {series_url}. Trying another selector...")
            # Thử một selector khác nếu cần
            product_cards = series_soup.select('.feature-card')

        for card in product_cards:
            gpu_info = {}
            
            # Lấy tên GPU
            name_tag = card.select_one('h2.name') or card.select_one('h3.title')
            if name_tag:
                gpu_info['name'] = name_tag.text.strip().replace('GeForce ', '')
            else:
                continue # Bỏ qua nếu không có tên

            print(f"Found GPU: {gpu_info['name']}")
            
            # Tìm link "View Full Specs" để lấy thông số chi tiết
            spec_link_tag = card.find('a', text=re.compile(r'View (Full )?Specs', re.IGNORECASE))
            if not spec_link_tag or not spec_link_tag.has_attr('href'):
                print(f"  - No spec link found for {gpu_info['name']}")
                # Thử lấy thông số ngay trên card nếu có
                gpu_info['chipset'] = "N/A"
                gpu_info['vram'] = "N/A"
                # ... thêm các thông số khác nếu có thể lấy từ card
                all_gpus.append(gpu_info)
                continue

            spec_url = base_url + spec_link_tag['href']
            print(f"  - Fetching specs from: {spec_url}")
            
            try:
                spec_page = requests.get(spec_url, headers=headers)
                spec_page.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"    - Error fetching spec page: {e}")
                continue

            spec_soup = BeautifulSoup(spec_page.content, 'html.parser')
            
            # Trích xuất thông số từ bảng "Full Specifications"
            # Đây là phần phức tạp nhất vì cấu trúc bảng có thể khác nhau
            gpu_info['chipset'] = gpu_info['name'] # Giả định chipset là tên
            
            # Hàm helper để tìm thông số trong bảng
            def find_spec(spec_name_regex):
                try:
                    # Tìm thẻ <th> hoặc <td> chứa tên thông số
                    header = spec_soup.find(lambda tag: tag.name in ['th', 'td'] and re.search(spec_name_regex, tag.text, re.IGNORECASE))
                    if header:
                        # Lấy thẻ anh em liền kề (là giá trị)
                        value_tag = header.find_next_sibling(['td', 'th'])
                        return value_tag.text.strip()
                except Exception:
                    return None
            
            # Lấy các thông số quan trọng
            vram = find_spec(r'Standard Memory Config')
            if vram:
                gpu_info['vram'] = vram
            else:
                gpu_info['vram'] = "N/A"

            # Bạn có thể thêm các thông số khác ở đây
            gpu_info['boost_clock'] = find_spec(r'Boost Clock \(GHz\)')
            gpu_info['length'] = find_spec(r'Length')
            gpu_info['tdp'] = find_spec(r'Graphics Card Power \(W\)')
            
            # Làm sạch dữ liệu (ví dụ: chỉ lấy số từ '12 GB GDDR6X')
            if isinstance(gpu_info.get('vram'), str):
                match = re.search(r'(\d+)\s*GB', gpu_info['vram'])
                if match:
                    gpu_info['vram'] = int(match.group(1))

            if isinstance(gpu_info.get('tdp'), str):
                match = re.search(r'(\d+)', gpu_info['tdp'])
                if match:
                    gpu_info['tdp'] = int(match.group(1))

            all_gpus.append(gpu_info)
            print(f"  - Specs extracted: {gpu_info}")

    return all_gpus

if __name__ == '__main__':
    nvidia_gpus = scrape_nvidia_gpus()
    
    if nvidia_gpus:
        # Lưu vào file JSON
        with open('nvidia_gpus.json', 'w', encoding='utf-8') as f:
            json.dump(nvidia_gpus, f, indent=4, ensure_ascii=False)
        print(f"\nSuccessfully scraped {len(nvidia_gpus)} NVIDIA GPUs and saved to nvidia_gpus.json")
    else:
        print("\nScraping failed. No data was saved.")