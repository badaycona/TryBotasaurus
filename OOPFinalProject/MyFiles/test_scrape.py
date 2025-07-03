import requests
import json

def get_raw_game_requirements(app_id: str):
    """
    Lấy thông tin cấu hình (dưới dạng HTML thô) của một game từ Steam Store API.

    Args:
        app_id: ID của game trên Steam.

    Returns:
        Một tuple chứa (cấu hình tối thiểu, cấu hình đề nghị) dưới dạng chuỗi HTML,
        hoặc (None, None) nếu không tìm thấy.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    
    try:
        response = requests.get(url)
        # Tự động báo lỗi nếu request không thành công (vd: lỗi 404, 500)
        response.raise_for_status() 
        
        data = response.json()
        
        # Kiểm tra xem app_id có hợp lệ và có dữ liệu trả về không
        if data and data[app_id].get('success'):
            game_data = data[app_id].get('data', {})
            
            # Lấy thông tin cấu hình PC
            pc_requirements = game_data.get('pc_requirements', {})
            
            # .get() sẽ trả về None nếu key không tồn tại, tránh gây lỗi
            min_req = pc_requirements.get('minimum')
            rec_req = pc_requirements.get('recommended')
            
            print(f"--- Lấy dữ liệu thành công cho game: {game_data.get('name')} ---")
            return min_req, rec_req
        else:
            print(f"Không tìm thấy dữ liệu hoặc yêu cầu không thành công cho AppID: {app_id}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Lỗi kết nối hoặc HTTP: {e}")
        return None, None
    except KeyError:
        print(f"Lỗi: Không tìm thấy AppID '{app_id}' trong dữ liệu trả về. Có thể AppID không đúng.")
        return None, None
    except json.JSONDecodeError:
        print("Lỗi: Không thể phân tích dữ liệu JSON từ Steam.")
        return None, None

# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    # AppID của ELDEN RING là 1245620
    # Bạn có thể thay bằng AppID của game khác
    game_id = "1245620" 
    
    minimum_html, recommended_html = get_raw_game_requirements(game_id)
    
    if minimum_html:
        print("\n=== CẤU HÌNH TỐI THIỂU (HTML THÔ) ===")
        print(minimum_html)
        
    if recommended_html:
        print("\n=== CẤU HÌNH ĐỀ NGHỊ (HTML THÔ) ===")
        print(recommended_html)