from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.image import Image
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.metrics import dp
from datas.main_flow import search_component
import os
import json
import sys
from models.hardwares import CPU, GPU, Mainboard, RAM, PSU, OS
from models.pc import PC
import requests
from game_requirement import *
from bs4 import BeautifulSoup
from get_image import get_image
import re

class BuildCheckApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATAS_DIR = os.path.join(self.BASE_DIR, 'datas')
        self.dialog = None
        self.pc_config = None

        # Define all hardware types and their filenames
        self.component_files = {
            'cpu':      ('cpu.json',      CPU),
            'gpu':      ('gpu.json',      GPU),
            'ram':      ('ram.json',      RAM),
            'mainboard':('mainboard.json',Mainboard),
            'psu':      ('psu.json',      PSU),
            'os':       ('os.json',       OS)
        }

        self.data = {}
        for key, (filename, cls) in self.component_files.items():
            loaded = self.load_component(filename)
            print(f"[DEBUG] Loaded {len(loaded)} {key.upper()}s. Example: {loaded[0] if loaded else 'No data'}")
            self.data[key] = {'data': loaded, 'class': cls, 'menu': None}

        # For backward compatibility with old attribute names
        self.cpu_data = self.data['cpu']['data']
        self.gpu_data = self.data['gpu']['data']
        self.ram_data = self.data['ram']['data']
        self.mainboard_data = self.data['mainboard']['data']
        self.psu_data = self.data['psu']['data']
        self.os_data = self.data['os']['data']

        # Load games cache
        self.game_data = self.load_component('steam_games_cache.json')
        print(f"Loaded {len(self.game_data)} games from cache.")
        self.game_menu = None
        self.search_trigger = None
        self.selected_game = None
    def show_component_specs(self, component_type, component_name):
        result = search_component(component_type, component_name)
        if "error" in result:
            self.show_error_dialog(result["error"])
        else:
            # Display result in your UI, e.g., in a dialog or label
            self.show_info_dialog(json.dumps(result, indent=2, ensure_ascii=False))

    def show_info_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Thông tin linh kiện",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()

    def load_component(self, filename):
        """Load a JSON component file from datas folder, fallback to pc-part-dataset if missing.
        Handles new format: dict with a single key whose value is a list.
        """
        datas_path = os.path.join(self.DATAS_DIR, filename)
        pc_part_path = os.path.join(self.BASE_DIR, '..', 'pc-part-dataset', 'data', 'json', filename)

        # Special case for steam_games_cache.json: keep as dict
        if filename == "steam_games_cache.json":
            for path in [datas_path, pc_part_path]:
                if os.path.exists(path):
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            d = json.load(file)
                            if isinstance(d, dict):
                                return d
                    except Exception as e:
                        print(f"Error loading {path}: {e}", file=sys.stderr)
            return {}

        # For hardware: handle new format
        def extract_list(d):
            if isinstance(d, list):
                return d
            if isinstance(d, dict):
                # If dict with 1 key, take its value
                if len(d) == 1:
                    v = next(iter(d.values()))
                    if isinstance(v, list):
                        return v
                    # If value is not a list, wrap in list
                    return [v]
                # If dict with multiple keys, flatten all values that are lists
                result = []
                for v in d.values():
                    if isinstance(v, list):
                        result.extend(v)
                    else:
                        result.append(v)
                return result
            return []

        data = []
        for path in [datas_path, pc_part_path]:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        d = json.load(file)
                        data.extend(extract_list(d))
                except Exception as e:
                    print(f"Error loading {path}: {e}", file=sys.stderr)
        return data

    def build(self):
        # Use os.path.join for all kv file paths
        gui_dir = os.path.join(self.BASE_DIR, 'gui')
        Builder.load_file(os.path.join(gui_dir, 'home_screen.kv'))
        Builder.load_file(os.path.join(gui_dir, 'pc_input_screen.kv'))
        Builder.load_file(os.path.join(gui_dir, 'select_game_screen.kv'))
        Builder.load_file(os.path.join(gui_dir, 'compatibility_screen.kv'))
        Builder.load_file(os.path.join(gui_dir, 'details_screen.kv'))
        return Builder.load_file(os.path.join(gui_dir, 'main.kv'))

    # def load_component(self, file_path):
    #     try:
    #         if os.path.exists(file_path):
    #             with open(file_path, 'r', encoding='utf-8') as file:
    #                 data = json.load(file)
    #                 return data
    #         else:
    #             print(f"File not found: {file_path}", file=sys.stderr)
    #             return []
    #     except Exception as e:
    #         print(f"Error loading {file_path}: {e}", file=sys.stderr)
    #         return []

    def set_screen(self, name):
        self.root.ids.screen_manager.current = name
    
    def on_profile(self):
        print("Hồ sơ người dùng")

    def on_settings(self):
        print("Mở cài đặt")
    
    def clear_pc_input(self):
        for screen in self.root.ids.screen_manager.screens:
            if screen.name == 'pc_input':
                for widget in screen.walk():
                    if isinstance(widget, MDTextField):
                        widget.text = ''
                break


    def show_exit_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Xác nhận thoát",
                text="Bạn muốn thoát ứng dụng?",
                buttons=[
                    MDFlatButton(
                        text="HỦY", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="THOÁT", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.stop()
                    ),
                ],
            )
        self.dialog.open()
    
    def on_component_model_text(self, component_type,  text_field):
        
        if self.search_trigger:
            self.search_trigger.cancel()

        # Lên lịch gọi hàm tìm kiếm sau 0.4 giây
        self.search_trigger = Clock.schedule_once(
            lambda dt: self.show_component_suggestions(component_type, text_field), 0.4
        )


    def show_component_suggestions(self, component_type, text_field):
        search_text = text_field.text.strip().lower()
        search_keywords = search_text.split()
        # Use the loaded data for suggestions (just names)
        filtered_names = [
            item['name']
            for item in self.data[component_type]['data']
            if all(keyword in item['name'].lower() for keyword in search_keywords)
        ]

        menu_items = [
            {
                "text": name,
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=name: self.select_component_by_name(text_field, x, component_type)
            } for name in filtered_names
        ]

        if self.data[component_type]['menu']:
            self.data[component_type]['menu'].dismiss()

        self.data[component_type]['menu'] = MDDropdownMenu(
            caller=text_field,
            items=menu_items,
            width_mult=4,
            max_height=dp(300),
            position="bottom",
        )
        if menu_items:
            self.data[component_type]['menu'].open()

    def select_component_by_name(self, text_field, component_name, component_type):
        # Fetch full specs using the new search_component logic
        specs = search_component(component_type, component_name)
        if "error" in specs:
            self.show_error_dialog(specs["error"])
            return

        screen = self.root.ids.screen_manager.get_screen('pc_input')

        if component_type == 'cpu':
            screen.ids.cpu_model.text = specs.get('name', component_name)
            screen.ids.cpu_cores.text = str(specs.get('core_count', ''))
            screen.ids.cpu_socket.text = specs.get('socket', '')
            screen.ids.cpu_tdp.text = str(specs.get('tdp', ''))
            screen.ids.cpu_coreclock.text = str(specs.get('core_clock', ''))
            screen.ids.cpu_boost.text = str(specs.get('boost_clock', ''))
        elif component_type == 'gpu':
            screen.ids.gpu_model.text = specs.get('name', component_name)
            screen.ids.gpu_vram.text = str(specs.get('vram', ''))
            screen.ids.gpu_boostclock.text = str(specs.get('boost_clock', ''))
            screen.ids.gpu_tdp.text = str(specs.get('tdp', ''))
            screen.ids.gpu_chipset.text = specs.get('chipset', '')
            screen.ids.gpu_coreclock.text = str(specs.get('core_clock', ''))
            screen.ids.gpu_length.text = str(specs.get('length', ''))
            screen.ids.gpu_color.text = specs.get('color', '')
        elif component_type == 'ram':
            screen.ids.ram_model.text = specs.get('name', component_name)
            screen.ids.ram_capa.text = str(specs.get('capacity', ''))
            screen.ids.speed_ram.text = str(specs.get('speed', ''))
            screen.ids.ram_type.text = specs.get('type', '')
            screen.ids.ram_color.text = specs.get('color', '')
        elif component_type == 'mainboard':
            screen.ids.mainboard_model.text = specs.get('name', component_name)
            screen.ids.mainboard_socket.text = specs.get('socket', '')
            screen.ids.mainboard_form.text = specs.get('form_factor', '')
            screen.ids.mainboard_chipset.text = specs.get('chipset', '')
            screen.ids.mainboard_ramtype.text = specs.get('ram_type', '')
            screen.ids.pcie.text = specs.get('pcie_version', '')
            screen.ids.mainboard_max.text = str(specs.get('max_memory', ''))
            screen.ids.slots.text = str(specs.get('memory_slots', ''))
            screen.ids.mainboard_color.text = specs.get('color', '')
        elif component_type == 'psu':
            screen.ids.psu_model.text = specs.get('name', component_name)
            screen.ids.psu_wattage.text = str(specs.get('wattage', ''))
        elif component_type == 'os':
            screen.ids.os.text = specs.get('name', component_name)

        if self.data[component_type]['menu']:
            self.data[component_type]['menu'].dismiss()

        # Optionally show a dialog with all specs
        self.show_component_specs(component_type, component_name)
      
    def validate_required_fields(self):
        screen = self.root.ids.screen_manager.get_screen('pc_input')

        # Danh sách các trường bắt buộc
        required_fields = {
            'cpu_model': screen.ids.cpu_model,
            'gpu_model': screen.ids.gpu_model,
            'ram_model': screen.ids.ram_model,
            'mainboard_model': screen.ids.mainboard_model,
            'psu_model': screen.ids.psu_model,

        }

        is_valid = True

        for field_id, field in required_fields.items():
            if not field.text.strip():
                # Nếu trống, hiển thị lỗi
                field.error = True
                field.helper_text = "Trường bắt buộc!"
                field.helper_text_mode = "on_error"
                is_valid = False
            else:
                # Nếu hợp lệ, xóa thông báo lỗi
                field.error = False
                field.helper_text = ""
                field.helper_text_mode = "on_focus"
        

        return is_valid
    def check_pc_compatibility(self):
        if not self.validate_required_fields():
            return

        screen = self.root.ids.screen_manager.get_screen('pc_input')
        # Tạo đối tượng PC từ dữ liệu nhập
        
        cpu = CPU(
            name=screen.ids.cpu_model.text,
            core_count=int(float(screen.ids.cpu_cores.text)),
            socket=screen.ids.cpu_socket.text,
            tdp=int(float(screen.ids.cpu_tdp.text)),
            core_clock=float(screen.ids.cpu_coreclock.text),
            boost_clock=screen.ids.cpu_boost.text
        )

        gpu = GPU(
            name=screen.ids.gpu_model.text,
            memory=screen.ids.gpu_vram.text,
            boost_clock=screen.ids.gpu_boostclock.text,
            tdp=int(float(screen.ids.gpu_tdp.text)),
            chipset=screen.ids.gpu_chipset.text,
            core_clock=int(float(screen.ids.gpu_coreclock.text)),
            length=int(float(screen.ids.gpu_length.text)),
            color=screen.ids.gpu_color.text
        )
        ram = RAM(
            name=screen.ids.ram_model.text,
            capacity=int(float(screen.ids.ram_capa.text)),
            speed=screen.ids.speed_ram.text,
            ram_type=screen.ids.ram_type.text,
            color=screen.ids.ram_color.text
        )
        mainboard = Mainboard(
            name=screen.ids.mainboard_model.text,
            socket=screen.ids.mainboard_socket.text,
            form_factor=screen.ids.mainboard_form.text,
            chipset=screen.ids.mainboard_chipset.text,
            ram_type=screen.ids.mainboard_ramtype.text ,
            pcie_version=screen.ids.pcie.text,
            max_memory=screen.ids.mainboard_max.text,
            memory_slots=screen.ids.slots.text,
            color=screen.ids.mainboard_color.text
        )
        psu = PSU(
            name=screen.ids.psu_model.text,
            wattage=int(float(screen.ids.psu_wattage.text))
        )
        os=screen.ids.os.text
        

        pc = PC(cpu, gpu, ram, mainboard, psu, os)
        result = pc.check_compatible()
        total_price = pc.total_cost()
        if total_price is not None:
            price_str = f"{total_price:,.0f} VND"
        else:
            price_str = "Không có thông tin giá"
        screen.ids.compatibility_text.text = f"{result}\nTổng giá: {price_str}"
        screen.ids.compatibility_result.md_bg_color = [0.2, 0.8, 0.2, 1] if result == "Cấu hình tương thích!" else [1, 0.2, 0.2, 1]

    # Kiem tra dau vao hop le, neu ko hien canh bao
    def on_submit_pc_input(self):
        if self.validate_required_fields():
            screen = self.root.ids.screen_manager.get_screen('pc_input')
            ids = screen.ids
            self.pc_config = {
                'OS': ids.os.text.strip(),
                'CPU': ids.cpu_model.text.strip(),
                'CPU_CoreClock': ids.cpu_coreclock.text.strip(),
                'CPU_BoostClock': ids.cpu_boost.text.strip(),
                'CPU_Cores': ids.cpu_cores.text.strip(),
                'RAM': ids.ram_capa.text.strip(),
                'GPU': ids.gpu_model.text.strip(),
                "GPU_chipset": ids.gpu_chipset.text.strip(),
                'GPU_VRAM': ids.gpu_vram.text.strip(),
                'Mainboard': ids.mainboard_model.text.strip(),
                'PSU': ids.psu_wattage.text.strip(),
            }    
            print(f"Cấu hình PC đã lưu: {self.pc_config}") 
            screen_table = self.root.ids.screen_manager.get_screen('compatibility')
            screen_table.ids.cpu_name.text=self.pc_config['CPU']
            screen_table.ids.pc_ram.text=self.pc_config['RAM'] + ' GB'
            screen_table.ids.pc_gpu.text=self.pc_config['GPU_chipset']
            screen_table.ids.os.text=self.pc_config['OS']

        else:         
            self.show_error_dialog("Điền đầy đủ các dòng bắt buộc !!!!")
    def show_error_dialog(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Thiếu thông tin",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK", text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                )
            ],
        )
        self.dialog.open()
    def search_games(self, search_text):
        """Tìm kiếm game dựa trên văn bản nhập và cập nhật RecycleView."""
        search_text = search_text.strip().lower()
        search_keywords = search_text.split()
        if isinstance(self.game_data, dict):
            filtered_games = [
                {"text": name, "app_id": app_id}
                for name, app_id in self.game_data.items()
                if all(keyword in name.lower() for keyword in search_keywords)
            ]
        else:
            filtered_games = []
        try:
            screen = self.root.ids.screen_manager.get_screen('select_game')
            screen.ids.game_list.data = [
                {
                    "text": game["text"],
                    "on_press": lambda x=game["app_id"], y=game["text"]: self.select_game(y, x)
                }
                for game in filtered_games
            ]
        except Exception as e:
            print(f"Không cập nhật được danh sách game: {e}")
    
    def update_suggestions(self, search_text):
        if hasattr(self, 'search_trigger') and self.search_trigger:
            self.search_trigger.cancel()
        self.show_game_suggestions(search_text)
    def select_game(self, game_name, app_id):
        """Cập nhật thông tin game được chọn."""
        try:
            screen = self.root.ids.screen_manager.get_screen('select_game')
            ids = screen.ids
        except Exception as e:
            print(f"Không truy cập được screen hoặc ids: {e}")
            return

        # Lấy dữ liệu game từ cache hoặc API
        game_data = self.get_structured_game_requirements(str(app_id))
        if not game_data:
            ids.game_name.text = "Lỗi: Không lấy được dữ liệu game"
            ids.game_image.source = "gpu.jpg"
            ids.game_requirements.text = "Không có thông tin cấu hình"
            return

        min_req = None
        min_req_text = "Không có thông tin cấu hình tối thiểu."
        if game_data.get('minimum'):
            try:
                min_req = self.from_str_to_object(game_data['minimum'])
                min_req_text = (
                    f"Cấu hình tối thiểu:\n"
                    f"OS: {min_req.OS}\n"
                    f"CPU: {min_req.CPU}\n"
                    f"RAM: {min_req.RAM}\n"
                    f"GPU: {min_req.GPU}\n"
                    f"DirectX: {min_req.DirectX}\n"
                    f"Storage: {min_req.Storage}"
                )
            except Exception as e:
                print(f"Lỗi khi xử lý yêu cầu tối thiểu: {e}")

        

        self.selected_game = Game(
            Name=game_data.get('name', 'Unknow'),
            Minimum=min_req,
            Image=get_image(str(app_id))
        )

        ids.game_name.text = self.selected_game.Name
        ids.game_image.source = self.selected_game.Image
        ids.game_requirements.text = min_req_text

    def show_game_suggestions(self, search_text):
        search_text = search_text.strip().lower()
        search_keywords = search_text.split()
        if isinstance(self.game_data, dict):
            filtered_games = [
                {"text": name, "app_id": app_id}
                for name, app_id in self.game_data.items()
                if all(keyword in name.lower() for keyword in search_keywords)
            ]
        else:
            filtered_games = []

        print(f"Filtering games with keywords: {search_keywords}, found: {len(filtered_games)}")  # Debug

        screen = self.root.ids.screen_manager.get_screen('select_game')
        text_field = screen.ids.get('game_input', None)
        if not text_field:
            print("Không tìm thấy trường nhập game.")
            return

        if self.game_menu:
            self.game_menu.dismiss()

        self.menu_game_buffer = {}

        menu_items = []
        for idx, game in enumerate(filtered_games):
            self.menu_game_buffer[idx] = game
            menu_items.append({
                "text": game["text"],
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda idx=idx: self.on_game_selected(idx)
            })

        self.game_menu = MDDropdownMenu(
            caller=text_field,
            items=menu_items,
            width_mult=4,
            max_height=dp(300),
            position="bottom",
        )

        if menu_items:
            self.game_menu.open()
        else:
            print("No menu items to show.")

    def on_game_selected(self, idx):
        if self.game_menu:
            self.game_menu.dismiss()

        game = self.menu_game_buffer.get(idx)
        if not game:
            print("Không tìm thấy game trong buffer.")
            return

        game_name = game["text"]
        app_id = game["app_id"]

        if not hasattr(self, 'root') or not self.root:
            print("Root widget không tồn tại.")
            return

        try:
            screen_manager = self.root.ids.get('screen_manager')
            if not screen_manager:
                print("ScreenManager không tồn tại trong ids.")
                return

            screen = screen_manager.get_screen('select_game')
            if not screen:
                print("Màn hình select_game không tồn tại.")
                return

            ids = screen.ids
            if 'game_input' in ids:
                ids['game_input'].text = game_name
            self.select_game(game_name, app_id)
        except Exception as e:
            print(f"Không truy cập được screen hoặc ids: {e}")

    def get_structured_game_requirements(self, app_id: str):
        url = "https://store.steampowered.com/api/appdetails?appids=" + app_id +'&l=en'
    
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            data = response.json()
            
            if data and data.get(app_id, {}).get('success'):
                game_data = data[app_id]['data']
                pc_requirements_html = game_data.get('pc_requirements', {})
                print(pc_requirements_html)
                min_req_html = pc_requirements_html.get('minimum')
                
                min_req_dict = self.parse_requirements_html(min_req_html)
                
                
                print(f"--- Lấy và xử lý dữ liệu thành công cho game: {game_data.get('name')} ---")
                return {'name': game_data.get('name'),
                    "minimum": min_req_dict
                    
                }
            else:
                print(f"Không tìm thấy dữ liệu hoặc yêu cầu không thành công cho AppID: {app_id}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối hoặc HTTP: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Lỗi xử lý dữ liệu hoặc AppID không hợp lệ: {e}")
            return None
    
    def parse_requirements_html(self, html_string: str) -> dict:
        """
        Phân tích chuỗi HTML cấu hình game thành một dictionary Python.
        """
        if not html_string:
            return {}
        
        soup = BeautifulSoup(html_string, 'html.parser')
        requirements = {}
        
        list_items = soup.find_all('li')
        
        for item in list_items:
            text = item.get_text(strip=True)
            
            if ':' in text:
                key, value = text.split(':', 1)
                key = key.strip()
                value = value.strip()
                requirements[key] = value
                
        return requirements
    def from_str_to_object(self, str_requirements : dict):
        try:
            OS_s = str_requirements.get('OS') or str_requirements.get('OS *') or str_requirements.get('ОС *')
        except KeyError:
            OS_s = "Unknown"
        CPU_s = str_requirements['Processor']
        RAM_s = str_requirements['Memory']
        GPU_s = str_requirements['Graphics']
        DirectX = str_requirements['DirectX']
        Storage = str_requirements['Storage']
        AdditionalNotes = str_requirements.get('Additional Notes', '')


        return Requirement( CPU_s, RAM_s, GPU_s, DirectX, Storage, OS_s, AdditionalNotes)
        
    def check_compatibility(self):
        """Chuyển sang CompatibilityScreen."""
        if not self.selected_game:
            try:
                current_screen = self.root.ids.screen_manager.current
                if current_screen == 'pc_input':
                    screen = self.root.ids.screen_manager.get_screen('pc_input')
                    screen.ids.compatibility_text.text = "Vui lòng chọn một game trước!"
                elif current_screen == 'select_game':
                    screen = self.root.ids.screen_manager.get_screen('select_game')
                    screen.ids.game_name.text = "Vui lòng chọn một game trước!"
                self.root.ids.screen_manager.current = 'select_game'
                return
            except Exception as e:
                print(f"Lỗi khi hiển thị thông báo: {e}")
                return

        self.on_submit_pc_input()  # Lưu cấu hình PC

        try:
            screen = self.root.ids.screen_manager.get_screen('compatibility')
            screen.ids.game_title.text = f"So Sánh Cấu Hình: {self.selected_game.Name}"
            print(f"self.pc_config trước khi chuyển: {self.pc_config}")  # Debug
            game_min=self.selected_game.Minimum
            screen.ids.game_os.text=game_min.OS
            screen.ids.game_cpu.text=game_min.CPU
            screen.ids.game_gpu.text=game_min.GPU
            screen.ids.free.text=game_min.Storage
            screen.ids.game_directx.text=game_min.DirectX
            screen.ids.game_ram.text=game_min.RAM
        except Exception as e:
            print(f"Lỗi khi cập nhật CompatibilityScreen: {e}")
        self.root.ids.screen_manager.current = 'compatibility'
    
if __name__ == '__main__':
    BuildCheckApp().run()
