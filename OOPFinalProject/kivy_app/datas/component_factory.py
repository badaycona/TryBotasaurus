# File: component_factory.py

import re
from hardwares import CPU, GPU, RAM, Mainboard, PSU, HardWareComponent

def _to_float(s):
    """Chuyển đổi chuỗi thành float, trả về 0.0 nếu thất bại."""
    if not s or not isinstance(s, str):
        return 0.0
    try:
        # Loại bỏ các ký tự không phải số (trừ dấu chấm)
        cleaned_s = re.sub(r'[^\d.]', '', s)
        return float(cleaned_s)
    except (ValueError, TypeError):
        return 0.0

def _to_int(s):
    """Chuyển đổi chuỗi thành int, trả về 0 nếu thất bại."""
    if not s or not isinstance(s, str):
        return 0
    try:
        # Tìm tất cả các chữ số trong chuỗi và ghép chúng lại
        digits = ''.join(re.findall(r'\d+', s))
        return int(digits) if digits else 0
    except (ValueError, TypeError):
        return 0
        
def _get_first_if_list(value):
    """Nếu giá trị là một danh sách, trả về phần tử đầu tiên, nếu không trả về chính nó."""
    if isinstance(value, list) and value:
        return value[0]
    return value


def _create_cpu_from_specs(specs: dict) -> CPU:
    """Tạo một đối tượng CPU từ dictionary thông số."""
    return CPU(
        name=_get_first_if_list(specs.get("Part #", "Unknown")), # Sử dụng Part # làm tên định danh
        price=_to_float(specs.get("price", "0")),
        core_count=_to_int(specs.get("Core Count", "0")),
        socket=specs.get("Socket", "Unknown"),
        tdp=_to_int(specs.get("TDP", "0 W")),
        core_clock=_to_float(specs.get("Performance Core Clock", "0 GHz")),
        boost_clock=_to_float(specs.get("Performance Core Boost Clock", "0 GHz")),
        graphics=specs.get("Integrated Graphics", "N/A"),
        smt=_get_first_if_list(specs.get("Simultaneous Multithreading", "N/A"))
    )

def _create_gpu_from_specs(specs: dict) -> GPU:
    """Tạo một đối tượng GPU từ dictionary thông số."""
    return GPU(
        name=specs.get("Model", "Unknown"),
        price=_to_float(specs.get("price", "0")),
        memory=_to_int(specs.get("Memory", "0 GB")),
        chipset=specs.get("Chipset", "Unknown"),
        tdp=_to_int(specs.get("TDP", "0 W")),
        core_clock=_to_int(specs.get("Core Clock", "0 MHz")),
        boost_clock=_to_int(specs.get("Boost Clock", "0 MHz")),
        length=_to_int(specs.get("Length", "0 mm")),
        color=specs.get("Color", "Unknown")
    )
    
def _create_ram_from_specs(specs: dict) -> RAM:
    """Tạo một đối tượng RAM từ dictionary thông số."""
    # Xử lý chuỗi "Modules" để lấy tổng dung lượng
    modules_str = specs.get("Modules", "1 x 0GB")
    capacity = 0
    if isinstance(modules_str, str):
        match = re.match(r'(\d+)\s*x\s*(\d+)\s*GB', modules_str)
        if match:
            num_modules, size_per_module = map(int, match.groups())
            capacity = num_modules * size_per_module

    return RAM(
        name=specs.get("product_name", "Unknown"),
        price=_to_float(specs.get("price", "0")),
        capacity=capacity,
        speed=_to_int(specs.get("Speed", "DDR5-0")),
        ram_type="DDR5" if "DDR5" in specs.get("Speed", "DDR5") else "DDR4", # Suy luận đơn giản
        color=specs.get("Color", "Unknown"),
        modules=modules_str,
        price_per_gb=_to_float(specs.get("Price / GB", "0")),
        first_word_latency=_to_float(specs.get("First Word Latency", "0 ns")),
        cas_latency=_to_int(specs.get("CAS Latency", "0"))
    )

def _create_motherboard_from_specs(specs: dict) -> Mainboard:
    """Tạo một đối tượng Mainboard từ dictionary thông số."""
    return Mainboard(
        name=specs.get("product_name", "Unknown"),
        price=_to_float(specs.get("price", "0")),
        socket=specs.get("Socket / CPU", "Unknown"),
        form_factor=specs.get("Form Factor", "Unknown"),
        chipset=specs.get("Chipset", "Unknown"),
        ram_type=specs.get("Memory Type", "Unknown"),
        max_memory=_to_int(specs.get("Memory Max", "0 GB")),
        memory_slots=_to_int(specs.get("Memory Slots", "0")),
        color=specs.get("Color", "Unknown"),
        pcie_version="Unknown" # Cần thêm logic để trích xuất từ PCIe x16 Slots nếu cần
    )

def _create_psu_from_specs(specs: dict) -> PSU:
    """Tạo một đối tượng PSU từ dictionary thông số."""
    return PSU(
        name=specs.get("product_name", "Unknown"),
        price=_to_float(specs.get("price", "0")),
        wattage=_to_int(specs.get("Wattage", "0 W")),
        efficiency=specs.get("Efficiency Rating", "Unknown"),
        color=specs.get("Color", "Unknown"),
        type=specs.get("Type", "Unknown"),
        modular=specs.get("Modular", "Unknown")
    )


# "Nhà máy" chính để tạo đối tượng
def create_component_object(specs: dict) -> HardWareComponent | None:
    """
    Tạo một đối tượng component cụ thể dựa trên loại sản phẩm trong dictionary specs.

    Args:
        specs (dict): Dictionary chứa các thông số được phân tích từ HTML.

    Returns:
        Một instance của class tương ứng (CPU, GPU, etc.) hoặc None nếu không nhận dạng được.
    """
    product_type = specs.get("product_type")

    # Bản đồ giữa loại sản phẩm và hàm tạo đối tượng tương ứng
    factory_map = {
        "cpu": _create_cpu_from_specs,
        "video-card": _create_gpu_from_specs,
        "memory": _create_ram_from_specs,
        "motherboard": _create_motherboard_from_specs,
        "power-supply": _create_psu_from_specs
    }

    # Lấy hàm tạo từ bản đồ
    creation_function = factory_map.get(product_type)

    if creation_function:
        return creation_function(specs)
    else:
        print(f"Cảnh báo: Không có hàm tạo nào cho loại sản phẩm '{product_type}'.")
        return None