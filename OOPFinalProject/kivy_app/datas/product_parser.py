import json
from bs4 import BeautifulSoup

SPECS_TO_EXTRACT = {
    "cpu": ["Manufacturer", "Part #", "Series", "Microarchitecture", "Core Family", "Socket", "Core Count", "Thread Count", "Performance Core Clock", "Performance Core Boost Clock", "L2 Cache", "L3 Cache", "TDP", "Integrated Graphics", "Maximum Supported Memory", "ECC Support", "Includes Cooler", "Packaging", "Lithography", "Simultaneous Multithreading"],
    "memory": ["Manufacturer", "Part #", "Speed", "Form Factor", "Modules", "Price / GB", "Color", "First Word Latency", "CAS Latency", "Voltage", "Timing", "ECC / Registered", "Heat Spreader"],
    "motherboard": ["Manufacturer", "Part #", "Socket / CPU", "Form Factor", "Chipset", "Memory Max", "Memory Type", "Memory Slots", "Memory Speed", "Color", "PCIe x16 Slots", "PCIe x1 Slots", "M.2 Slots", "SATA 6.0 Gb/s Ports", "Onboard Ethernet", "Onboard Video", "USB 2.0 Headers", "USB 3.2 Gen 1 Headers", "USB 3.2 Gen 2 Headers", "Supports ECC", "Wireless Networking", "RAID Support", "Uses Back-Connect Connectors"],
    "power-supply": ["Manufacturer", "Part #", "Type", "Efficiency Rating", "Wattage", "Length", "Modular", "Color", "Fanless", "ATX 4-pin Connectors", "EPS 8-pin Connectors", "PCIe 16-pin 12VHPWR/12V-2x6 Connectors", "PCIe 12-pin Connectors", "PCIe 8-pin Connectors", "PCIe 6+2-pin Connectors", "PCIe 6-pin Connectors", "SATA Connectors", "AMP/Molex 4-pin Connectors"],
    "video-card": ["Manufacturer", "Model", "Part #", "Chipset", "Memory", "Memory Type", "Core Clock", "Boost Clock", "Effective Memory Clock", "Interface", "Color", "Frame Sync", "Length", "TDP", "Case Expansion Slot Width", "Total Slot Width", "Cooling", "External Power", "HDMI Outputs", "DisplayPort Outputs"]
}

def parse_html_for_specs(html_content: str, url: str) -> dict:
    """
    Phân tích nội dung HTML của một trang sản phẩm để trích xuất các thông số kỹ thuật.

    Args:
        html_content (str): Mã nguồn HTML của trang.
        url (str): URL gốc của trang để tham chiếu.

    Returns:
        dict: Một dictionary chứa các thông số kỹ thuật đã được trích xuất.
    """
    soup = BeautifulSoup(html_content, 'lxml')

    # 1. Trích xuất Tên và Loại Sản phẩm
    product_name_tag = soup.select_one("h1.pageTitle")
    product_name = product_name_tag.get_text(strip=True) if product_name_tag else "N/A"
    
    breadcrumb_tags = soup.select("section.breadcrumb ol li a")
    product_type_text = "unknown"
    if breadcrumb_tags:
        product_type_text = breadcrumb_tags[-1].get_text(strip=True)

    product_type_key = product_type_text.lower().replace(" ", "-")

    specs_result = {
        "product_name": product_name, 
        "product_type": product_type_key, 
        "url": url
    }

    found_specs = {}
    spec_groups = soup.select("div.specs > div.group--spec")

    for group in spec_groups:
        title_tag = group.select_one("h3.group__title")
        content_tag = group.select_one("div.group__content")
        
        if title_tag and content_tag:
            title = title_tag.get_text(strip=True)
            
            list_items = content_tag.select("ul > li")
            if list_items:
                values = [li.get_text(strip=True) for li in list_items]
                found_specs[title] = values
            else:
                found_specs[title] = content_tag.get_text(strip=True)

    if product_type_key in SPECS_TO_EXTRACT:
        target_spec_list = SPECS_TO_EXTRACT[product_type_key]
        for spec_name in target_spec_list:
            specs_result[spec_name] = found_specs.get(spec_name, "N/A")
    else:
        print(f"Cảnh báo: Không nhận dạng được loại sản phẩm '{product_type_key}' cho URL {url}. Sẽ trích xuất tất cả thông số tìm thấy.")
        specs_result.update(found_specs)

    return specs_result

if __name__ == '__main__':
    example_files = [
        'example_cpu.html',
        'example_motherboard.html',
        'example_memory.html',
        'example_video_card.html',
        'example_power_supply.html',
    ]

    for filename in example_files:
        print("-" * 50)
        print(f"Đang xử lý file: {filename}")
        print("-" * 50)
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                html = f.read()
            
            dummy_url = f"https://pcpartpicker.com/product/example/{filename}"
            
            product_specs = parse_html_for_specs(html, dummy_url)
            
            print(json.dumps(product_specs, indent=4))

        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file '{filename}'. Vui lòng đảm bảo file tồn tại trong cùng thư mục.")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi xử lý file '{filename}': {e}")