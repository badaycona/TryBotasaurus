# --- File ví dụ: try_scrape.py ---

# Import các class cần thiết
from pypartpicker.client import Client
from pypartpicker.retriever import SeleniumRetriever # <-- Import class mới

def main():
    # 1. Khởi tạo SeleniumRetriever
    retriever = SeleniumRetriever()
    
    # 2. Chạy thiết lập ban đầu.
    #    Hàm này sẽ tạm dừng và đợi bạn giải CAPTCHA.
    retriever.initial_setup("https://uk.pcpartpicker.com/")
    
    # 3. Khởi tạo Client, truyền phương thức get_response vào.
    pcpp_client = Client(response_retriever=retriever.get_response)
    
    # 4. Bây giờ bạn có thể sử dụng client như bình thường.
    #    Tất cả các yêu cầu sẽ sử dụng session đã được xác thực.
    try:
        print("\nBắt đầu tìm kiếm 'ryzen 5' ở UK...")
        search_result = pcpp_client.get_part_search("ryzen 5", region="uk")
        
        if search_result and search_result.parts:
            print(f"Tìm thấy {len(search_result.parts)} kết quả trên trang {search_result.page}/{search_result.total_pages}.")
            for part in search_result.parts[:5]: # In 5 kết quả đầu tiên
                price_str = str(part.cheapest_price) if part.cheapest_price else "N/A"
                print(f"- {part.name} ({price_str})")
        else:
            print("Không tìm thấy kết quả nào.")

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình scraping: {e}")

if __name__ == "__main__":
    main()