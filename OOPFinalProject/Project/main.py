# main.py
from scrapers import scrape_cpus

if __name__ == "__main__":
    print("Bắt đầu quy trình cào dữ liệu PCPartPicker...")
    print("-" * 30)
    
    scrape_cpus()
    print("-" * 30)

    
    
    print("Đã hoàn thành tất cả các tác vụ cào dữ liệu!")
    print("Dữ liệu đã được lưu trong thư mục 'output/'.")