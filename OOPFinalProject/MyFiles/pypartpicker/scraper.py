# --- START OF FILE scraper.py ---

from typing import Optional
from requests_html import HTML
import urllib.parse
from .types import (
    Part,
    Rating,
    Vendor,
    Price,
    PartList,
    PartSearchResult,
    Review,
    User,
    PartReviewsResult,
)
from .urls import *
from .regex import *
from requests import Response


class Scraper:
    def __init__(self):
        pass

    def __get_base_url(self, region: str) -> str:
        """Tạo URL cơ sở dựa trên khu vực."""
        if region == "us":
            return "https://pcpartpicker.com"
        return f"https://{region}.pcpartpicker.com"

    def is_rate_limit_from_content(self, html_content: str) -> bool:
        """Kiểm tra rate limit của PCPartPicker từ nội dung HTML thô."""
        html = HTML(html=html_content)
        title = html.find(".pageTitle", first=True)
        if title is None:
            title_tag = html.find("title", first=True)
            return title_tag is not None and title_tag.text == "Unavailable"
        return title.text == "Verification"

    def prepare_part_url(self, id_url: str, region: str = None) -> str:
        """Chuẩn bị URL đầy đủ cho một sản phẩm từ ID hoặc URL."""
        match = PRODUCT_URL_RE.match(id_url)
        if match is None:
            url = ID_RE.match(id_url)
            if url is None:
                raise ValueError("Invalid pcpartpicker product URL or ID.")
            id_url = url.group(1)
            region = "us"
        else:
            region = "us" if match.group(2) is None else match.group(2)[:-1]
            id_url = match.group(3)

        if id_url is None:
            raise ValueError("Invalid pcpartpicker product URL or ID.")

        return self.__get_base_url(region) + PRODUCT_PATH + id_url

    def parse_part(self, res: Response) -> Part:
        """Phân tích cú pháp trang chi tiết của một sản phẩm."""
        html: HTML = HTML(html=res.text, url=res.url)
        title_container = html.find(".wrapper__pageTitle", first=True)
        sidebar = html.find(".sidebar-content", first=True)

        if not title_container or not sidebar:
            raise ValueError("Could not parse part page. HTML structure might have changed or page is invalid.")

        type = title_container.find(".breadcrumb", first=True).text
        name = title_container.find(".pageTitle", first=True).text

        # Lấy đánh giá
        rating = None
        star_container = title_container.find(".product--rating", first=True)
        if star_container:
            stars = (
                len(star_container.find(".shape-star-full"))
                + len(star_container.find(".shape-star-half")) * 0.5
            )
            rating_text_element = title_container.find("p:has(.product--rating)", first=True)
            if rating_text_element:
                rating_info = PRODUCT_RATINGS_RE.search(rating_text_element.text)
                if rating_info:
                    count, average = rating_info.groups()
                    rating = Rating(stars, int(count), float(average))

        # Lấy thông số kỹ thuật
        specs = {}
        specs_block = sidebar.find(".specs", first=True)
        if specs_block:
            for spec in specs_block.find(".group--spec"):
                spec_title_el = spec.find(".group__title", first=True)
                spec_value_el = spec.find(".group__content", first=True)
                if spec_title_el and spec_value_el:
                    specs[spec_title_el.text] = spec_value_el.text

        # Lấy URL hình ảnh
        image_urls = []
        thumbnails = sidebar.find(".product__image-2024-thumbnails", first=True)
        if thumbnails is None:
            main_image = sidebar.find(".product__image-2024 img", first=True)
            if main_image and 'src' in main_image.attrs:
                image_urls.append("https:" + main_image.attrs["src"])
        else:
            for image in thumbnails.find("img"):
                if 'src' in image.attrs and ".256p.jpg" in image.attrs['src']:
                    image_base_url = "https:" + image.attrs["src"].split(".256p.jpg")[0]
                    image_urls.append(image_base_url + ".1600.jpg")

        # Lấy danh sách nhà cung cấp và giá
        vendors = []
        price_table = html.find("#prices table tbody", first=True)
        if price_table:
            for row in price_table.find("tr:not(.tr--noBorder)"):
                try:
                    vendor_image = row.find(".td__logo img", first=True)
                    if not vendor_image: continue
                    
                    base_price_raw = row.find(".td__base", first=True).text
                    base_price_search = DECIMAL_RE.search(base_price_raw)
                    if not base_price_search: continue
                    
                    base_price = base_price_search.group()
                    currency = base_price_raw.replace(base_price, "").strip()

                    final_price_link = row.find(".td__finalPrice a", first=True)
                    if not final_price_link: continue
                    
                    total_price = final_price_link.text.replace(currency, "").strip().removesuffix("+")

                    vendors.append(Vendor(
                        name=vendor_image.attrs["alt"],
                        logo_url="https:" + vendor_image.attrs["src"],
                        in_stock=row.find(".td__availability--inStock", first=True) is not None,
                        price=Price(
                            base=float(base_price),
                            discounts=float(row.find(".td__promo", first=True).text.replace(currency, "").strip() or "0"),
                            shipping=float(DECIMAL_RE.search(row.find(".td__shipping", first=True).text).group() if "FREE" not in row.find(".td__shipping", first=True).text.upper() and DECIMAL_RE.search(row.find(".td__shipping", first=True).text) else "0"),
                            tax=float(row.find(".td__tax", first=True).text.replace(currency, "").strip() or "0"),
                            total=float(total_price),
                            currency=currency,
                        ),
                        buy_url=final_price_link.attrs["href"],
                    ))
                except (AttributeError, ValueError, IndexError) as e:
                    print(f"Warning: Could not parse a vendor row. Error: {e}")
                    continue

        cheapest_price = None
        in_stock_globally = False
        available_vendors = [v for v in vendors if v.in_stock]
        if available_vendors:
            in_stock_globally = True
            cheapest_price = min(available_vendors, key=lambda v: v.price.total).price

        # Lấy các bài đánh giá trên trang
        base_url = "https://" + urllib.parse.urlparse(res.url).netloc
        reviews = [self.parse_review(review, base_url) for review in html.find(".partReviews .partReviews__review")]

        return Part(
            name=name, type=type, image_urls=image_urls, url=res.url,
            cheapest_price=cheapest_price, in_stock=in_stock_globally,
            vendors=vendors, rating=rating, specs=specs, reviews=reviews,
        )

    def parse_review(self, review: HTML, base_url: str) -> Review:
        """Phân tích cú pháp một khối HTML chứa đánh giá."""
        user_details = review.find(".userDetails", first=True)
        if not user_details: return None # Bỏ qua nếu không có user details
        
        avatar_url_el = user_details.find("img", first=True)
        avatar_url = avatar_url_el.attrs["src"] if avatar_url_el and 'src' in avatar_url_el.attrs else ''
        if avatar_url.startswith("//"):
            avatar_url = "https:" + avatar_url
        elif avatar_url and not avatar_url.startswith("http"):
            avatar_url = base_url + avatar_url

        name_container = user_details.find(".userDetails__userName a", first=True)
        profile_url = base_url + name_container.attrs["href"] if name_container and 'href' in name_container.attrs else ''
        username = name_container.text if name_container else 'Unknown'

        user_data = user_details.find(".userDetails__userData", first=True)
        points_text = user_data.find("li:first-child", first=True) if user_data else None
        points = int(points_text.text.split(" ")[0]) if points_text and points_text.text.split(" ")[0].isdigit() else 0
        created_at_el = user_data.find("li:last-child", first=True) if user_data else None
        created_at = created_at_el.text if created_at_el else ''

        review_name = review.find(".partReviews__name", first=True)
        stars = len(review_name.find(".product--rating .shape-star-full")) if review_name else 0

        build_name, build_url = None, None
        build_a = review_name.find("a", first=True) if review_name else None
        if build_a and 'href' in build_a.attrs:
            build_name = build_a.text
            build_url = base_url + build_a.attrs["href"]

        content_el = review.find(".partReviews__writeup", first=True)
        content = content_el.text if content_el else ''

        return Review(
            author=User(username, avatar_url, profile_url),
            points=points, stars=stars, created_at=created_at,
            content=content, build_name=build_name, build_url=build_url,
        )

    def prepare_part_reviews_url(self, id_url: str, page: int = 1, rating: Optional[int] = None):
        """Chuẩn bị URL cho trang đánh giá sản phẩm."""
        base = self.prepare_part_url(id_url)
        if rating is None:
            return f"{base}{PART_REVIEWS_PATH}?page={page}"
        return f"{base}{PART_REVIEWS_PATH}?page={page}&rating={rating}"

    def parse_reviews(self, res: Response) -> PartReviewsResult:
        """Phân tích cú pháp trang đánh giá sản phẩm."""
        html: HTML = HTML(html=res.text, url=res.url)
        base_url = "https://" + urllib.parse.urlparse(res.url).netloc
        reviews = [self.parse_review(review, base_url) for review in html.find(".partReviews .partReviews__review")]

        pagination = html.find("#module-pagination", first=True)
        current_page, total_pages = 0, 0
        if pagination:
            current_page_el = pagination.find(".pagination--current", first=True)
            if current_page_el: current_page = int(current_page_el.text)
            
            last_page_el = pagination.find("li:last-child a", first=True)
            if last_page_el and last_page_el.text.isdigit():
                total_pages = int(last_page_el.text)
            elif current_page > 0:
                total_pages = current_page # Giả định là trang cuối nếu không tìm thấy

        return PartReviewsResult(reviews=[r for r in reviews if r is not None], page=current_page, total_pages=total_pages)

    def prepare_part_list_url(self, id_url: str, region: str = None) -> str:
        """Chuẩn bị URL cho một danh sách linh kiện."""
        match = PART_LIST_URL_RE.match(id_url)
        override_region = region
        if match is None:
            url = ID_RE.match(id_url)
            if url is None: raise ValueError("Invalid pcpartpicker part list URL or ID.")
            id_url = url.group(1)
            region = "us"
        else:
            region = "us" if match.group(2) is None else match.group(2)[:-1]
            id_url = match.group(3)
        if override_region: region = override_region
        if id_url is None: raise ValueError("Invalid pcpartpicker part list URL or ID.")
        return self.__get_base_url(region) + PART_LIST_PATH + id_url

    def parse_part_list(self, res: Response) -> PartList:
        """Phân tích cú pháp một trang danh sách linh kiện."""
        html: HTML = HTML(html=res.text, url=res.url)
        # ... (Toàn bộ logic của hàm này được giữ nguyên, vì nó đã hoạt động với HTML object)
        # ... Đây là một hàm rất phức tạp, tôi sẽ không dán lại toàn bộ để tránh quá dài,
        # ... nhưng bạn chỉ cần đảm bảo nó bắt đầu bằng dòng `html: HTML = ...`
        return PartList(...) # Trả về kết quả

    def prepare_search_url(self, query: str, page: int, region: Optional[str] = "us"):
        """Chuẩn bị URL cho trang tìm kiếm."""
        return (
            self.__get_base_url("us" if region is None else region)
            + SEARCH_PATH
            + f"?q={urllib.parse.quote(query)}&page={page}"
        )

    def parse_part_search(self, res: Response) -> PartSearchResult:
        """Phân tích cú pháp trang kết quả tìm kiếm."""
        html: HTML = HTML(html=res.text, url=res.url)
        page_title = html.find(".pageTitle", first=True)
        
        # Xử lý trường hợp redirect sang trang sản phẩm
        if not page_title or "Search" not in page_title.text:
            try:
                part = self.parse_part(res)
                return PartSearchResult(parts=[part], page=1, total_pages=1)
            except Exception:
                return PartSearchResult(parts=[], page=0, total_pages=0)

        results = []
        for result in html.find(".search-results__pageContent li"):
            try:
                link = result.find(".search_results--link a", first=True)
                if not link: continue
                
                name = link.text
                url = "https://" + urllib.parse.urlparse(res.url).netloc + link.attrs["href"]
                
                image_el = result.find(".search_results--img img", first=True)
                image_url = "https:" + image_el.attrs["src"] if image_el and 'src' in image_el.attrs else None
                
                cheapest_price = None
                price_raw = result.find(".search_results--price", first=True)
                if price_raw and price_raw.text.strip():
                    price_text = price_raw.text.strip()
                    total_search = DECIMAL_RE.search(price_text)
                    if total_search:
                        total = total_search.group()
                        currency = price_text.replace(total, "").strip()
                        cheapest_price = Price(total=float(total), currency=currency)

                results.append(Part(
                    name=name, type=None, image_urls=[image_url] if image_url else [], url=url,
                    cheapest_price=cheapest_price, in_stock=cheapest_price is not None
                ))
            except (AttributeError, ValueError, IndexError) as e:
                print(f"Warning: Could not parse a search result item. Error: {e}")
                continue

        # Phân trang
        pagination = html.find("#module-pagination", first=True)
        current_page, total_pages = 1, 1
        if pagination:
            current_page_el = pagination.find(".pagination--current", first=True)
            if current_page_el: current_page = int(current_page_el.text)
            
            last_page_el = pagination.find("li a")[-1] if pagination.find("li a") else None
            if last_page_el and last_page_el.text.isdigit():
                total_pages = int(last_page_el.text)
            elif current_page > 1 and not last_page_el:
                 total_pages = current_page

        return PartSearchResult(parts=results, page=current_page, total_pages=total_pages)
        
    def prepare_browse_url(self, product_path: str, page: int, region: Optional[str] = "us"):
        """Chuẩn bị URL cho yêu cầu AJAX duyệt sản phẩm."""
        if product_path not in PRODUCT_PATHS:
            raise ValueError(f"Đường dẫn sản phẩm không hợp lệ: {product_path}")
        region = "us" if region is None else region
        base_url = self.__get_base_url(region)
        # URL cho AJAX thường chỉ là URL gốc của danh mục
        return f"{base_url}{PRODUCTS_PATH}{product_path}/"

    def parse_product_browse_ajax(self, res: Response) -> tuple[list[Part], int, int]:
        """Phân tích cú pháp kết quả JSON trả về từ yêu cầu AJAX của trang danh mục."""
        try:
            data = res.json()
            # Cấu trúc JSON có thể là data['result']['html']
            result_data = data.get('result', data) 
            html_content = result_data.get('html', '')
            pagination_html = result_data.get('pagination', '')
        except Exception as e:
            print(f"Lỗi khi parse JSON: {e}")
            print("--- NỘI DUNG PHẢN HỒI TỪ SERVER ---")
            print(res.text[:1000]) # In ra để debug
            print("------------------------------------")
            return [], 0, 0
            
        html: HTML = HTML(html=html_content)
        table = html.find("tbody", first=True)
        if not table:
            return [], 0, 0
            
        base_url = "https://" + urllib.parse.urlparse(res.url).netloc
        
        parts = []
        for row in table.find("tr"):
            name_cell = row.find(".td__name", first=True)
            if not name_cell or not name_cell.find("a", first=True):
                continue

            name = name_cell.text.strip()
            part_url = base_url + name_cell.find("a", first=True).attrs["href"]
            
            # Ở bước này chỉ cần lấy URL, không cần thông tin chi tiết
            parts.append(Part(name=name, type=None, url=part_url))

        # Phân tích cú pháp HTML của pagination
        pagination_html_obj = HTML(html=pagination_html)
        current_page_el = pagination_html_obj.find(".pagination--current", first=True)
        current_page = int(current_page_el.text) if current_page_el else 1
        
        total_pages = current_page
        page_links = pagination_html_obj.find("li a")
        if page_links:
            page_numbers = [int(a.text) for a in page_links if a.text.isdigit()]
            if page_numbers:
                total_pages = max(page_numbers)
                
        return parts, current_page, total_pages