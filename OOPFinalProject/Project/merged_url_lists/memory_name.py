import json
import re

def get_ram_name_from_url(url: str) -> str:
    """
    Trích xuất và định dạng tên RAM từ một URL của pcpartpicker.com.

    Args:
        url: Chuỗi URL đầu vào.

    Returns:
        Một chuỗi đã được định dạng là tên của RAM.
    """
    if not url:
        return ""

    try:
        slug = url.strip().split('/')[-1]
    except IndexError:
        return ""

    # Tách phần mô tả và mã sản phẩm (nếu có)
    # Từ "memory" là một dấu hiệu tốt để tách
    parts = slug.split('-memory-')
    name_slug = parts[0]
    model_code = parts[1] if len(parts) > 1 else ""

    # 1. Bắt đầu xử lý phần tên
    name_with_spaces = name_slug.replace('-', ' ')

    # 2. Định dạng các thông số kỹ thuật bằng regex trước khi viết hoa
    # Định dạng kit (ví dụ: "2 x 8 gb" -> "(2 x 8 GB)")
    name_with_spaces = re.sub(r'(\d+)\s+x\s+(\d+)\s+gb', r'(\1 x \2 GB)', name_with_spaces, flags=re.IGNORECASE)
    # Định dạng dung lượng đơn (ví dụ: "16 gb" -> "16 GB")
    name_with_spaces = re.sub(r'\b(\d+)\s+gb\b', r'\1 GB', name_with_spaces, flags=re.IGNORECASE)
    
    # 3. Viết hoa các từ
    formatted_name = name_with_spaces.title()

    # 4. Áp dụng các hiệu chỉnh về chữ hoa cho các từ đặc biệt
    # Chuyển "Ddr4" thành "DDR4", "Cl16" thành "CL16", v.v.
    formatted_name = re.sub(r'\bDdr(\d)\b', r'DDR\1', formatted_name)
    formatted_name = re.sub(r'\bCl(\d+)\b', r'CL\1', formatted_name)
    
    acronyms = [
        'RGB', 'AMD', 'LED', 'TUF', 'OCZ', 'LPX', 
        'SO-DIMM', 'DIMM', 'ECC', 'VLP'
    ]
    for acronym in acronyms:
        # Sử dụng re.IGNORECASE để xử lý các biến thể như 'rgb', 'Rgb', 'RGB'
        formatted_name = re.sub(r'\b' + re.escape(acronym) + r'\b', acronym, formatted_name, flags=re.IGNORECASE)

    # 5. Kết hợp lại với mã sản phẩm
    if model_code:
        final_name = f"{formatted_name} Memory {model_code.upper()}"
    else:
        # Nếu không có phần model_code, đảm bảo từ "Memory" có ở cuối
        if not formatted_name.endswith('Memory'):
            final_name = f"{formatted_name} Memory"
        else:
            final_name = formatted_name

    return final_name.strip()


def create_memory_json_from_file(input_filename: str, output_filename: str):
    """
    Đọc các URL từ file đầu vào, tạo tên RAM và ghi kết quả
    dưới dạng key-value vào một file JSON.

    Args:
        input_filename: Tên của file chứa danh sách URL RAM.
        output_filename: Tên của file JSON sẽ được tạo.
    """
    memory_database = {}
    print(f"Đang đọc từ file: {input_filename}...")

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url:
                    ram_name = get_ram_name_from_url(url)
                    if ram_name:
                        memory_database[ram_name] = url
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{input_filename}'. Vui lòng đảm bảo file tồn tại.")
        return
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi đọc file: {e}")
        return

    print(f"Đã xử lý {len(memory_database)} URL.")

    # Ghi dictionary vào file JSON
    try:
        with open(output_filename, 'w', encoding='utf-8') as f_json:
            json.dump(memory_database, f_json, indent=4, ensure_ascii=False)
        print(f"Thành công! Dữ liệu đã được ghi vào file '{output_filename}'.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghi file JSON: {e}")


# --- Chạy chương trình ---
if __name__ == "__main__":
    INPUT_FILE = "memory_urls_merged.txt"
    OUTPUT_FILE = "memory_data.json"
    create_memory_json_from_file(INPUT_FILE, OUTPUT_FILE)