import requests
import json
import time

def build_steam_games_dictionary(cache_file="steam_games_cache.json"):
    """
    Tải danh sách tất cả các ứng dụng từ Steam và xây dựng một dictionary
    với key là tên game (viết thường) và value là AppID.
    Hàm này cũng lưu kết quả vào một file cache để tránh gọi API liên tục.
    """
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    
    print("Đang tải danh sách game từ Steam API...")
    
    try:
        response = requests.get(url, timeout=30) 
        response.raise_for_status()
        data = response.json()
        
        apps = data.get("applist", {}).get("apps", [])
        
        if not apps:
            print("Không nhận được danh sách game từ API.")
            return None
            
        game_dict = {app['name'].lower(): app['appid'] for app in apps if app['name']}
        
        print(f"Đã xây dựng thành công dictionary với {len(game_dict)} game/ứng dụng.")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(game_dict, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu dictionary vào file '{cache_file}'")
            
        return game_dict

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API Steam: {e}")
        return None
    except json.JSONDecodeError:
        print("Lỗi khi phân tích dữ liệu JSON trả về.")
        return None

def load_games_from_cache(cache_file="steam_games_cache.json"):
    """
    Tải dictionary game từ file cache nếu có.
    """
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            print(f"Đã tải dictionary từ cache '{cache_file}'.")
            return json.load(f)
    except FileNotFoundError:
        print("Không tìm thấy file cache. Sẽ tiến hành tải mới từ API.")
        return None
    except json.JSONDecodeError:
        print("File cache bị lỗi. Sẽ tiến hành tải mới từ API.")
        return None

if __name__ == "__main__":
    steam_games = load_games_from_cache()
    
    if not steam_games:
        steam_games = build_steam_games_dictionary()

    if steam_games:
        game_name_to_find = "elden ring" 
        
        app_id = steam_games.get(game_name_to_find)
        
        if app_id:
            print(f"\nTìm thấy! AppID của '{game_name_to_find.title()}' là: {app_id}")
        else:
            print(f"\nKhông tìm thấy game có tên chính xác là '{game_name_to_find.title()}'")
            
        game_name_to_find_2 = "counter-strike 2"
        app_id_2 = steam_games.get(game_name_to_find_2)
        if app_id_2:
             print(f"Tìm thấy! AppID của '{game_name_to_find_2.title()}' là: {app_id_2}")
        else:
             print(f"Không tìm thấy game có tên chính xác là '{game_name_to_find_2.title()}'")