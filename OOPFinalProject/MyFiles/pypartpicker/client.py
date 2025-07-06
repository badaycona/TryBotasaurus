# --- START OF FILE client.py (Phiên bản Cloudscraper ban đầu) ---

import cloudscraper
from .scraper import Scraper
from .types import Part, PartList, PartSearchResult, PartReviewsResult
from .errors import CloudflareException, RateLimitException
from requests import Response
from typing import Optional
import time

class Client:
    def __init__(
        self,
        max_retries=3,
        retry_delay=1,
        response_retriever=None,
    ):
        self.__scraper = Scraper()
        
        # SỬA ĐỔI QUAN TRỌNG: Cấu hình cloudscraper để giả mạo trình duyệt thật
        # Đây là bước nâng cấp từ phiên bản gốc để cố gắng vượt qua lỗi 403
        self.__session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Đoạn code này cho phép truyền một response_retriever tùy chỉnh,
        # nhưng chúng ta sẽ dùng cái mặc định.
        self.__get_response = (
            response_retriever
            if response_retriever is not None
            else self.__default_response_retriever
        )
        if not callable(self.__get_response):
            raise ValueError("response_retriever must be callable.")

    def __default_response_retriever(self, url: str, retries=0) -> Response:
        if retries >= self.max_retries:
            raise CloudflareException(f"Request to {url} failed, max retries exceeded.")

        try:
            print(f"Cloudscraper đang lấy dữ liệu từ: {url}")
            # Gửi yêu cầu bằng cloudscraper session
            res = self.__session.get(url)
            # Nếu request không thành công (vd: 403, 500), nó sẽ ném ra một exception
            res.raise_for_status()
        except Exception as e:
            # Bắt exception đó và thử lại
            print(f"Request to {url} failed with {e}. Retrying...")
            time.sleep(self.retry_delay * (retries + 1)) # Tăng thời gian chờ sau mỗi lần thử
            return self.__default_response_retriever(url, retries + 1)

        # Kiểm tra rate limit của chính PCPartPicker
        if self.__scraper.is_rate_limit_from_content(res.text):
            raise RateLimitException(f"PCPP rate limit encountered: {url}")

        return res

    def get_part(self, id_url: str, region: str = None) -> Part:
        url = self.__scraper.prepare_part_url(id_url, region)
        res = self.__get_response(url)
        return self.__scraper.parse_part(res)

    def get_part_list(self, id_url: str, region: str = None) -> PartList:
        url = self.__scraper.prepare_part_list_url(id_url, region)
        res = self.__get_response(url)
        return self.__scraper.parse_part_list(res)

    def get_part_search(
        self, query: str, page: int = 1, region: Optional[str] = None
    ) -> PartSearchResult:
        # Đây là hàm đã được gọi trong script thử nghiệm của bạn
        url = self.__scraper.prepare_search_url(query, page, region)
        res = self.__get_response(url)
        return self.__scraper.parse_part_search(res)

    def get_part_reviews(
        self, id_url: str, page: int = 1, rating: Optional[int] = None
    ) -> PartReviewsResult:
        url = self.__scraper.prepare_part_reviews_url(id_url, page, rating)
        res = self.__get_response(url)
        return self.__scraper.parse_reviews(res)