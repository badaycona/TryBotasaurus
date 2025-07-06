import json
import re

def get_psu_name_from_url(url: str) -> str:
    """
    Trích xuất và định dạng tên PSU từ một URL của pcpartpicker.com.

    Args:
        url: Chuỗi URL đầu vào.

    Returns:
        Một chuỗi đã được định dạng là tên của PSU.
    """
    if not url:
        return ""

    # 1. Lấy phần cuối cùng của URL (slug)
    try:
        slug = url.strip().split('/')[-1]
    except IndexError:
        return "" # Trả về chuỗi rỗng nếu URL không hợp lệ

    # 2. Thay thế dấu gạch nối bằng dấu cách
    name_with_spaces = slug.replace('-', ' ')

    # 3. Viết hoa chữ cái đầu mỗi từ
    formatted_name = name_with_spaces.title()

    # 4. Áp dụng các hiệu chỉnh cụ thể để có định dạng tốt hơn
    
    # Danh sách các từ viết tắt cần viết hoa hoàn toàn
    acronyms = [
        'Atx', 'Sfx', 'Tfx', 'Rgb', 'Tt', 'Na', 'Us', 'Uk', 'Eu', 'De',
        'Ii', 'Iii', 'V2', 'G2', 'G3', 'G5', 'G6', 'G7', 'P2', 'P3', 'P5', 'P6',
        'Csk', 'Rm', 'Rmx', 'Hx', 'Sf', 'Vs', 'Vs', 'Cx', 'Psu', 'Mpg', 'Meg', 'Rog',
        'Gf1', 'Gf3', 'Cpu', 'Gpu', 'Ocz'
    ]
    for acronym in acronyms:
        # Sử dụng \b để đảm bảo chúng ta chỉ thay thế toàn bộ từ
        formatted_name = re.sub(r'\b' + acronym + r'\b', acronym.upper(), formatted_name, flags=re.IGNORECASE)

    # Thêm dấu '+' cho các chứng nhận 80 Plus
    ratings = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Titanium']
    for rating in ratings:
        formatted_name = formatted_name.replace(f'80 {rating}', f'80+ {rating}')

    # Định dạng công suất (ví dụ: '750 W' -> '750W')
    formatted_name = re.sub(r'(\d+)\s+W\b', r'\1W', formatted_name)

    return formatted_name

def create_psu_json_from_file(input_filename: str, output_filename: str):
    """
    Đọc các URL từ file đầu vào, tạo tên PSU và ghi kết quả
    dưới dạng key-value vào một file JSON.

    Args:
        input_filename: Tên của file chứa danh sách URL.
        output_filename: Tên của file JSON sẽ được tạo.
    """
    # Dictionary để lưu trữ cặp key:value (tên PSU : URL)
    psu_database = {}

    print(f"Đang đọc từ file: {input_filename}...")

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                # Loại bỏ khoảng trắng và ký tự xuống dòng thừa
                url = line.strip()
                if url:
                    # Lấy tên PSU làm key
                    psu_name = get_psu_name_from_url(url)
                    
                    # Thêm vào dictionary với URL là value
                    if psu_name: # Đảm bảo tên không rỗng
                        psu_database[psu_name] = url
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{input_filename}'. Vui lòng đảm bảo file tồn tại.")
        return # Thoát khỏi hàm nếu không tìm thấy file
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi đọc file: {e}")
        return

    print(f"Đã xử lý {len(psu_database)} URL.")

    # Ghi dictionary vào file JSON
    try:
        with open(output_filename, 'w', encoding='utf-8') as f_json:
            # json.dump để ghi dữ liệu
            # indent=4 để file JSON dễ đọc hơn
            # ensure_ascii=False để hiển thị đúng các ký tự đặc biệt nếu có
            json.dump(psu_database, f_json, indent=4, ensure_ascii=False)
        print(f"Thành công! Dữ liệu đã được ghi vào file '{output_filename}'.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghi file JSON: {e}")

# --- Chạy chương trình ---
if __name__ == "__main__":
    INPUT_FILE = "supply_urls_merged.txt"
    OUTPUT_FILE = "psu_data.json"
    create_psu_json_from_file(INPUT_FILE, OUTPUT_FILE)