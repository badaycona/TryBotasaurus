import logging
from botasaurus.browser import browser, Driver, NotFoundException
from botasaurus.request import request, Request
from botasaurus.user_agent import UserAgent
from botasaurus.window_size import WindowSize

logger = logging.getLogger(__name__)

@browser(
    # proxy="http://119.28.74.177:10004",

    headless=False,
    
    profile="pcpartpicker_session_final",
    tiny_profile=True,
    user_agent=UserAgent.HASHED,
    window_size=WindowSize.HASHED,
    remove_default_browser_check_argument=True,

    # ĐÃ SỬA LẠI: Bật lại việc chặn tài nguyên ngay từ đầu.
    # Thử thách của Cloudflare vẫn hoạt động mà không cần tải ảnh/css.
    block_images_and_css=True, 
    
    reuse_driver=True,
    max_retry=2,
    close_on_crash=True,
    output=None,
)
def get_bypassed_page_source(driver: Driver, url: str) -> str:
    """
    Sử dụng một chiến lược nâng cao để vượt qua Cloudflare bằng cách mô phỏng
    hành vi nhấp chuột của con người.
    """
    logger.info(f"Đang lấy dữ liệu từ '{url}' bằng phương pháp vượt qua nâng cao...")

    driver.get(url)
    driver.long_random_sleep()

    if driver.is_in_page("Cloudflare") and driver.is_in_page("Verify you are human"):
        logger.warning("Phát hiện trang thử thách của Cloudflare. Bắt đầu quá trình giải quyết...")
        
        try:
            captcha_iframe = driver.select('iframe[title="Widget containing a Cloudflare security challenge"]')
            
            if not captcha_iframe:
                raise Exception("Không tìm thấy iframe của Cloudflare CAPTCHA.")

            driver.enable_human_mode()
            logger.info("Chế độ 'Human Mode' đã được kích hoạt.")

            checkbox = captcha_iframe.select("input[type=checkbox]")
            
            if not checkbox:
                 raise Exception("Không tìm thấy hộp kiểm bên trong iframe của Cloudflare.")
            
            checkbox.click()
            logger.info("Đã nhấp vào hộp kiểm CAPTCHA.")

            driver.long_random_sleep()
            driver.disable_human_mode()

        except Exception as e:
            logger.error(f"Quá trình giải quyết CAPTCHA thất bại: {e}")
            raise

    if driver.is_in_page("Cloudflare"):
        logger.error("Vẫn bị Cloudflare chặn sau khi đã thử giải quyết. Vui lòng kiểm tra lại proxy và selector.")
        raise Exception("Cloudflare detection persists after interaction.")
    
    logger.info(f"Vượt qua Cloudflare thành công! Đang lấy mã nguồn trang.")
    
    # ĐÃ XÓA: Xóa dòng code gây lỗi 'AttributeError'
    # driver.block_resources(['image', 'css']) 
    
    return driver.page_html

def close_browser_session():
    if hasattr(get_bypassed_page_source, 'close'):
        logger.info("Đang đóng session trình duyệt...")
        get_bypassed_page_source.close()
        logger.info("Session trình duyệt đã được đóng thành công.")

# Hàm request không thay đổi
@request(cache=False, max_retry=10, raise_exception=True, output=None)
def get_bypassed_page_source_request(req: Request, url: str) -> str:
    logger.info(f"Đang lấy dữ liệu từ '{url}' bằng phương pháp request nhẹ...")
    try:
        response = req.get(url)
        if response.status_code == 404:
            logger.warning(f"Không tìm thấy trang (404) tại: {url}")
            raise NotFoundException(f"Trang trả về lỗi 404: {url}")
        
        response.raise_for_status()
        logger.info(f"Lấy dữ liệu thành công từ '{url}' với mã trạng thái {response.status_code}.")
        return response.text
    except Exception as e:
        logger.error(f"Đã xảy ra lỗi khi lấy dữ liệu từ '{url}' bằng request nhẹ: {e}")
        raise