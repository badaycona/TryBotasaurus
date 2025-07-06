import json
import os
import re

# ==============================================================================
# BỘ QUY TẮC ĐỊNH DẠNG TÊN (NÂNG CAO)
# ==============================================================================

GPU_BRANDS = {'msi', 'gigabyte', 'asus', 'evga', 'zotac', 'sapphire', 'xfx', 'powercolor', 'palit', 'gainward', 'pny', 'inno3d', 'galax', 'kfa2', 'colorful', 'yeston', 'amd', 'nvidia', 'intel', 'asrock', 'visiontek', 'diamond', 'club-3d', 'acer', 'onix', 'lenovo', 'hp', 'corsair', 'matrox', 'sparkle', 'dell', 'leadtek'}
CHIPSET_BRANDS = {'geforce', 'radeon', 'arc', 'quadro', 'firepro', 'tesla', 'titan'}
EDITIONS = {
    'oc': 'OC', 'super': 'Super', 'ti': 'Ti', 'xt': 'XT', 'xtx': 'XTX', 'le': 'LE',
    'gaming': 'GAMING', 'tuf': 'TUF', 'strix': 'STRIX', 'aorus': 'AORUS', 'ko': 'KO',
    'ventus': 'Ventus', 'suprim': 'SUPRIM', 'trio': 'Trio', 'pulse': 'Pulse', 'nitro': 'NITRO',
    'merc': 'MERC', 'swft': 'SWFT', 'qick': 'QICK', 'phantom': 'Phantom', 'eagle': 'Eagle',
    'vision': 'Vision', 'master': 'Master', 'extreme': 'XTREME', 'windforce': 'WindForce',
    'aero': 'AERO', 'armor': 'ARMOR', 'mech': 'MECH', 'challenger': 'Challenger',
    'fighter': 'Fighter', 'hellhound': 'Hellhound', 'devil': 'Devil', 'jetstream': 'JetStream',
    'phoenix': 'Phoenix', 'uprising': 'UPRISING', 'revel': 'REVEL', 'verto': 'Verto',
    'epic': 'EPIC-X', 'xlr8': 'XLR8', 'ftw': 'FTW', 'ftw3': 'FTW3', 'xc': 'XC', 'sc': 'SC',
    'ultra': 'Ultra', 'pro': 'PRO', 'founders': 'Founders Edition', 'dual': 'Dual',
    'proart': 'ProArt', 'white': 'White', 'black': 'Black', 'limited': 'Limited Edition',
    'evo': 'EVO', 'advanced': 'Advanced', 'classic': 'Classic', 'amp': 'AMP', 'core': 'Core',
    'mini': 'Mini', 'itx': 'ITX', 'slim': 'Slim', 'hybrid': 'Hybrid', 'liquid': 'Liquid',
    'blower': 'Blower', 'lp': 'LP', 'low': 'Low', 'profile': 'Profile',
    'waterforce': 'WaterForce', 'sakura': 'SAKURA', 'tf': 'Twin Frozr',
    'gddr5': 'GDDR5', 'gddr6': 'GDDR6', 'gddr6x': 'GDDR6X', 'hbm2': 'HBM2'
}

CHIPSET_MODEL_RE = re.compile(
    r'(?P<series>rtx|gtx|rx|gt|r\d|hd|arc)'
    r'[-_]?(?P<model>\d{3,4})'
    r'[-_]?(?P<suffix>ti|super|xt|xtx)?',
    re.IGNORECASE)

VRAM_RE = re.compile(r'(\d{1,2})(g|gb)')

def _build_name_from_parts(parts_dict):
    """Sắp xếp và xây dựng tên cuối cùng từ các thành phần đã được phân tích."""
    order = ['brand', 'chipset_brand', 'series_model', 'editions', 'memory', 'other']
    
    if 'editions' in parts_dict and parts_dict['editions']:
        # Sắp xếp các phiên bản để có thứ tự hợp lý hơn
        parts_dict['editions'] = ' '.join(sorted(list(set(parts_dict['editions'])), key=lambda x: (len(x), x)))

    final_name_parts = [parts_dict.get(key, '') for key in order]
    # Nối các phần lại, loại bỏ khoảng trắng thừa
    return ' '.join(filter(None, final_name_parts)).strip().replace('  ', ' ')

def _decode_mpn_string(mpn_part, parts_dict):
    """Cố gắng giải mã một chuỗi MPN (Mã Part Number của nhà sản xuất)."""
    original_mpn = mpn_part.upper()
    mpn_part = mpn_part.lower()

    # MSI/ASUS MPN style
    if mpn_part.startswith(('n', 'r', 'eah', 'engtx')):
        if not parts_dict['brand']:
            if mpn_part.startswith(('n', 'r')): parts_dict['brand'] = "MSI"
            if mpn_part.startswith(('eah', 'engtx')): parts_dict['brand'] = "ASUS"
        
        if not parts_dict['chipset_brand']:
            if mpn_part.startswith(('n', 'engtx')): parts_dict['chipset_brand'] = "GeForce"
            if mpn_part.startswith(('r', 'eah')): parts_dict['chipset_brand'] = "Radeon"
        
        model_match = re.search(r'(\d{3,4})', mpn_part)
        if model_match and not parts_dict['series_model']:
            model_num = model_match.group(1)
            # Đoán dòng dựa trên số model
            series = "Unknown"
            if model_num.startswith(('1','2','3','4','5')): series = "GeForce RTX/GTX"
            if model_num.startswith(('6','7','8','9')): series = "Radeon HD/R9/RX"
            parts_dict['series_model'] = f"{model_num}" # Sẽ được ghép với brand sau
        
        if 'tf' in mpn_part: parts_dict['editions'].append('Twin Frozr')
        if 'oc' in mpn_part: parts_dict['editions'].append('OC')
        vram_match = re.search(r'(\d)g[d]?', mpn_part)
        if vram_match and not parts_dict['memory']: parts_dict['memory'] = f"{vram_match.group(1)}GB"
        
        parts_dict['other'].append(original_mpn)
        return True
        
    return False

def format_gpu_name(slug):
    """Logic nâng cao để định dạng tên GPU."""
    parts_dict = {
        'brand': '', 'chipset_brand': '', 'series_model': '', 'memory': '',
        'editions': [], 'other': []
    }
    
    slug_parts = slug.lower().replace('video-card', '').replace('graphics-card', '').split('-')
    remaining_parts = []
    
    for part in slug_parts:
        if part in GPU_BRANDS:
            if not parts_dict['brand']: parts_dict['brand'] = part.upper() if part not in ['club-3d', 'inno3d'] else part.replace('-', ' ').title()
        elif part in CHIPSET_BRANDS:
            if not parts_dict['chipset_brand']: parts_dict['chipset_brand'] = part.capitalize()
        elif part in EDITIONS:
            parts_dict['editions'].append(EDITIONS[part])
        elif VRAM_RE.match(part):
            if not parts_dict['memory']: parts_dict['memory'] = f"{VRAM_RE.match(part).group(1)}GB"
        else:
            remaining_parts.append(part)
            
    found_model = False
    unprocessed_parts = []
    for part in remaining_parts:
        model_match = CHIPSET_MODEL_RE.search(part)
        if model_match and not found_model:
            series = model_match.group('series').upper()
            model_num = model_match.group('model')
            suffix = model_match.group('suffix') or ''
            
            # Xử lý các dòng cũ
            if series in ['R9', 'R7']:
                parts_dict['series_model'] = f"{series} {model_num} {suffix.capitalize()}".strip()
                if not parts_dict['chipset_brand']: parts_dict['chipset_brand'] = 'Radeon'
            elif series == 'HD':
                 parts_dict['series_model'] = f"HD {model_num} {suffix.capitalize()}".strip()
                 if not parts_dict['chipset_brand']: parts_dict['chipset_brand'] = 'Radeon'
            else:
                parts_dict['series_model'] = f"{series} {model_num} {suffix.capitalize()}".strip()
            found_model = True
        elif not found_model and _decode_mpn_string(part, parts_dict):
            found_model = True
        else:
            unprocessed_parts.append(part.upper())
            
    parts_dict['other'] = ' '.join(unprocessed_parts)
    return _build_name_from_parts(parts_dict)

def format_generic_name(slug):
    """Logic định dạng chung cho CPU và Motherboard."""
    ACRONYMS = {'CPU', 'GPU', 'AMD', 'INTEL', 'MSI', 'EVGA', 'ASUS', 'GIGABYTE', 'ASROCK', 'LGA', 'AM4', 'AM5', 'TR4', 'STRX4', 'ATX', 'ITX', 'WIFI', 'RTX', 'GTX', 'RX', 'OC', 'SE', 'RGB', 'DDR3', 'DDR4', 'DDR5', 'USB', 'GB', 'PRO', 'MAX', 'SLI', 'AC', 'WIFI6E', 'WIFI7', 'NVME', 'PCIE', 'SATA', 'HDMI', 'DP'}
    SPECIAL_CASES = {'ghz': 'GHz', 'thz': 'THz', 'ti': 'Ti'}
    
    words = slug.split('-')
    formatted_words = []
    for word in words:
        if not word: continue
        lower_word = word.lower()
        upper_word = word.upper()

        if lower_word in SPECIAL_CASES:
            formatted_words.append(SPECIAL_CASES[lower_word])
        elif upper_word in ACRONYMS:
            formatted_words.append(upper_word)
        elif word.isalnum() and not word.isalpha() and not word.isdigit():
            formatted_words.append(upper_word)
        else:
            formatted_words.append(word.capitalize())
    return ' '.join(formatted_words)


def process_file_key_value(input_filename, output_filename, component_type):
    """Hàm xử lý tệp chính."""
    if not os.path.exists(input_filename):
        print(f"Lỗi: Tệp '{input_filename}' không tồn tại.")
        return

    print(f"Đang xử lý '{input_filename}' cho {component_type}...")
    component_data = {}
    
    with open(input_filename, 'r', encoding='utf-8') as f:
        for url in f:
            url = url.strip()
            if not url: continue
            try:
                slug = url.split('/')[-1]
                
                if component_type == 'gpu':
                    name = format_gpu_name(slug)
                else:
                    name = format_generic_name(slug)
                
                if len(name) < 5:
                    name = format_generic_name(slug)

                if name in component_data:
                    original_name = name
                    counter = 2
                    while name in component_data:
                        name = f"{original_name} V{counter}"
                        counter += 1
                
                component_data[name] = url
            except Exception as e:
                print(f"  Lỗi khi xử lý URL {url}: {e}")

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(component_data, f, indent=4, ensure_ascii=False)

    print(f"-> Hoàn thành! Đã lưu kết quả vào '{output_filename}'.")


def main():
    """Hàm chính điều phối."""
    files_to_process = {
        "cpu": ("cpu_urls_merged.txt", "cpu_data_kv.json"),
        "motherboard": ("motherboard_urls_merged.txt", "motherboard_data_kv.json"),
        "gpu": ("card_urls_merged.txt", "gpu_data_kv.json")
    }

    for comp_type, (input_file, output_file) in files_to_process.items():
        process_file_key_value(input_file, output_file, comp_type)
        print("-" * 30)

if __name__ == "__main__":
    main()