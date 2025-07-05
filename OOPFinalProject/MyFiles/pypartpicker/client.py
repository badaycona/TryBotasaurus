# --- START OF FILE client.py ---

import asyncio
from .scraper import Scraper
from .types import Part, PartList, PartSearchResult, PartReviewsResult
from .errors import CloudflareException, RateLimitException
from requests import Response
from typing import Coroutine, Optional
# Bỏ các import không dùng đến

class Client:
    def __init__(
        self,
        # THAY ĐỔI: Bây giờ chúng ta yêu cầu một response_retriever
        response_retriever,
    ):
        if not callable(response_retriever):
            raise ValueError("response_retriever phải là một hàm hoặc phương thức có thể gọi được.")
            
        self.__scraper = Scraper()
        # __get_response bây giờ chính là phương thức get_response từ SeleniumRetriever
        self.__get_response = response_retriever

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
        url = self.__scraper.prepare_search_url(query, page, region)
        res = self.__get_response(url)
        return self.__scraper.parse_part_search(res)

    def get_part_reviews(
        self, id_url: str, page: int = 1, rating: Optional[int] = None
    ) -> PartReviewsResult:
        url = self.__scraper.prepare_part_reviews_url(id_url, page, rating)
        res = self.__get_response(url)
        return self.__scraper.parse_reviews(res)

# AsyncClient sẽ rất phức tạp để triển khai với Selenium,
# nên tôi sẽ tạm thời comment nó ra. Giải pháp tốt nhất là sử dụng Playwright-Python
# cho các tác vụ bất đồng bộ.
#
# class AsyncClient: ...