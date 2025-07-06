import os
import re
import json
from bs4 import BeautifulSoup

# --- CẤU HÌNH ---
# Thư mục chứa các file HTML đã tải về.
HTML_SOURCE_DIR = 'html_pages'
# URL cơ sở để tạo link sản phẩm đầy đủ.
BASE_URL = 'https://pcpartpicker.com'
# Thư mục để lưu trữ các file JSON đầu ra.
OUTPUT_DIR = 'component_data'

def group_files_by_component(source_dir: str) -> dict[str, list[str]]:
    """
    Quét một thư mục và nhóm các file HTML theo tên component.
    Tên component được trích xuất từ tên file, ví dụ: 'page_cpu_1.html' -> 'cpu'.

    Args:
        source_dir (str): Thư mục để quét.

    Returns:
        dict: Một dictionary trong đó key là tên component và value là danh sách các đường dẫn file.
              ví dụ: {'cpu': ['html_pages/page_cpu_1.html', 'html_pages/page_cpu_2.html']}
    """
    if not os.path.isdir(source_dir):
        print(f"Lỗi: Không tìm thấy thư mục nguồn '{source_dir}'.")
        return {}

    component_files = {}
    # Regex để trích xuất tên component từ tên file như 'page_cpu_1.html'
    # Nó tìm một từ (word) nằm giữa 'page_' và '_' theo sau là số.
    pattern = re.compile(r'page_([a-zA-Z0-9\-]+)_\d+\.html')

    for filename in os.listdir(source_dir):
        if filename.endswith('.html'):
            match = pattern.search(filename)
            if match:
                component_name = match.group(1)
                
                # Khởi tạo danh sách cho component này nếu đây là lần đầu tiên
                if component_name not in component_files:
                    component_files[component_name] = []
                
                # Thêm đường dẫn file đầy đủ vào danh sách
                full_path = os.path.join(source_dir, filename)
                component_files[component_name].append(full_path)

    return component_files

def parse_product_data_for_component(file_paths: list[str], base_url: str) -> dict[str, str]:
    """
    Phân tích một danh sách các file HTML và trả về một dictionary chứa
    tên sản phẩm và URL.

    Args:
        file_paths (list): Danh sách các đường dẫn file đầy đủ cho một component.
        base_url (str): URL cơ sở để tạo link đầy đủ.

    Returns:
        dict: Một dictionary chứa các cặp {tên_sản_phẩm: url_đầy_đủ}.
    """
    product_data = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except IOError as e:
            print(f"  - Cảnh báo: Không thể đọc file {file_path}. Lỗi: {e}")
            continue
            
        soup = BeautifulSoup(html_content, 'lxml')
        # Chọn tất cả các hàng (tr) trong bảng sản phẩm
        product_rows = soup.select("tbody#category_content > tr.tr__product")
        
        for row in product_rows:
            # Tìm thẻ 'a' chứa link và tên sản phẩm
            link_tag = row.select_one("td.td__name > a")
            # Tìm thẻ 'p' chứa tên sản phẩm sạch
            name_tag = row.select_one("p")

            if link_tag and name_tag:
                relative_url = link_tag.get('href')
                # Lấy text từ thẻ <p> và loại bỏ khoảng trắng thừa
                product_name = name_tag.get_text(strip=True)
                
                if relative_url and product_name:
                    full_url = base_url + relative_url
                    # Lưu vào dictionary, nếu tên đã tồn tại sẽ được ghi đè
                    # (thường không sao vì URL sẽ giống nhau)
                    product_data[product_name] = full_url

    return product_data


# --- Khối thực thi chính ---
if __name__ == "__main__":
    print("--- BẮT ĐẦU KỊCH BẢN PHÂN TÍCH HTML THEO COMPONENT ---")

    # 1. Nhóm tất cả các file HTML theo loại component
    grouped_files = group_files_by_component(HTML_SOURCE_DIR)

    if not grouped_files:
        print("Không tìm thấy file component nào để xử lý.")
    else:
        print(f"Tìm thấy {len(grouped_files)} component: {', '.join(grouped_files.keys())}")
        
        # Tạo thư mục đầu ra nếu nó chưa tồn tại
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # 2. Xử lý từng nhóm component
        for component, files in grouped_files.items():
            print(f"\n--- Đang xử lý component: {component} ({len(files)} file) ---")
            
            # 3. Trích xuất tất cả dữ liệu (tên, URL) cho component hiện tại
            component_data = parse_product_data_for_component(files, BASE_URL)
            
            if component_data:
                # 4. Lưu dữ liệu vào file JSON chuyên dụng
                output_filename = os.path.join(OUTPUT_DIR, f"{component}.json")
                
                try:
                    with open(output_filename, 'w', encoding='utf-8') as f:
                        # Sắp xếp các key (tên sản phẩm) để output nhất quán
                        sorted_data = dict(sorted(component_data.items()))
                        json.dump(sorted_data, f, indent=4, ensure_ascii=False)
                    
                    print(f"Thành công! Đã lưu {len(component_data)} sản phẩm vào '{output_filename}'")
                except IOError as e:
                     print(f"  - Lỗi: Không thể ghi vào file {output_filename}. Lỗi: {e}")
            else:
                print(f"Không tìm thấy dữ liệu sản phẩm nào cho component '{component}'.")

    print("\n--- KỊCH BẢN HOÀN TẤT ---")