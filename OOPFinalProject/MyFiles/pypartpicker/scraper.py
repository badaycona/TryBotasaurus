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
        if region == "us":
            return "https://pcpartpicker.com"

        return f"https://{region}.pcpartpicker.com"

    def is_cloudflare(self, res: Response) -> bool:
        # res bây giờ là requests_html.Response, nên .html hoạt động
        return res.html.find("title", first=True).text == "Just a moment..."
    
    # THÊM MỚI: Phương thức kiểm tra rate limit từ raw HTML content
    def is_rate_limit_from_content(self, html_content: str) -> bool:
        # Dùng cho client đồng bộ mới sử dụng cloudscraper
        html = HTML(html=html_content)
        title = html.find(".pageTitle", first=True)
        if title is None:
            title_tag = html.find("title", first=True)
            return title_tag is not None and title_tag.text == "Unavailable"
        return title.text == "Verification"

    def is_rate_limit(self, res: Response) -> bool:
        # Dùng cho AsyncClient cũ
        title = res.html.find(".pageTitle", first=True)
        if title is None:
            return res.html.find("title", first=True).text == "Unavailable"
        return title.text == "Verification"

    def prepare_part_url(self, id_url: str, region: str = None) -> str:
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
        # THAY ĐỔI: Tạo đối tượng HTML từ `res.text`
        html: HTML = HTML(html=res.text, url=res.url)
        title_container = html.find(".wrapper__pageTitle", first=True)
        sidebar = html.find(".sidebar-content", first=True)

        # ... (phần còn lại của hàm không thay đổi)
        # Part name and type
        type = title_container.find(".breadcrumb", first=True).text
        name = title_container.find(".pageTitle", first=True).text

        # Rating
        rating = None
        star_container = title_container.find(".product--rating", first=True)
        if star_container is not None:
            stars = (
                len(star_container.find(".shape-star-full"))
                + len(star_container.find(".shape-star-half")) * 0.5
            )
            rating_info = PRODUCT_RATINGS_RE.match(
                title_container.find("section div:has(ul)", first=True).text
            )
            count = rating_info.group(1)
            average = rating_info.group(2)
            rating = Rating(stars, int(count), float(average))

        # Specs
        specs = {}
        specs_block = sidebar.find(".specs", first=True)
        for spec in specs_block.find(".group--spec"):
            spec_title = spec.find(".group__title", first=True).text
            spec_value = spec.find(".group__content", first=True).text
            specs[spec_title] = spec_value

        # Images
        image_urls = []
        thumbnails = sidebar.find(".product__image-2024-thumbnails", first=True)
        if thumbnails is None:
            image_urls.append(
                "https:"
                + sidebar.find(".product__image-2024 img", first=True).attrs["src"]
            )
        else:
            for image in thumbnails.find("img"):
                image_base_url = "https:" + image.attrs["src"].split(".256p.jpg")[0]
                image_urls.append(image_base_url + ".1600.jpg")

        # Vendors
        vendors = []
        for row in html.find("#prices table tbody tr:not(.tr--noBorder)"):
            vendor_image = row.find(".td__logo img", first=True)
            logo_url = "https:" + vendor_image.attrs["src"]
            vendor_name = vendor_image.attrs["alt"]

            # Vendor price
            base_price_raw = row.find(".td__base", first=True).text
            base_price_search = DECIMAL_RE.search(base_price_raw)
            if not base_price_search: continue # Bỏ qua nếu không tìm thấy giá
            base_price = base_price_search.group()
            currency = base_price_raw.replace(base_price, "").strip()

            # Discounts, shipping, tax and total price
            promo = (
                row.find(".td__promo", first=True).text.replace(currency, "").strip()
            )
            if promo == "":
                promo = "0"

            shipping_raw = row.find(".td__shipping", first=True)
            shipping = (
                0
                if "FREE" in shipping_raw.text
                or shipping_raw.text.strip() == ""
                or shipping_raw.find("img", first=True) is not None
                else (DECIMAL_RE.search(shipping_raw.text).group() if DECIMAL_RE.search(shipping_raw.text) else 0)
            )
            tax = row.find(".td__tax", first=True).text.replace(currency, "").strip()
            if tax == "":
                tax = "0"

            final = row.find(".td__finalPrice a", first=True)
            total_price = final.text.replace(currency, "").strip().removesuffix("+")

            # Availability and buy url
            in_stock = row.find(".td__availability--inStock", first=True) is not None
            buy_url = final.attrs["href"]

            vendors.append(
                Vendor(
                    name=vendor_name,
                    logo_url=logo_url,
                    in_stock=in_stock,
                    price=Price(
                        base=float(base_price),
                        discounts=float(promo),
                        shipping=float(shipping),
                        tax=float(tax),
                        total=float(total_price),
                        currency=currency,
                    ),
                    buy_url=buy_url,
                )
            )

        cheapest_price = None
        in_stock = False

        available_vendors = list(filter(lambda v: v.in_stock, vendors))
        if len(available_vendors) > 0:
            in_stock = True
            cheapest_price = sorted(available_vendors, key=lambda v: v.price.total)[
                0
            ].price

        base_url = "https://" + urllib.parse.urlparse(res.url).netloc

        reviews = []
        for review in html.find(".partReviews .partReviews__review"):
            reviews.append(self.parse_review(review, base_url))

        return Part(
            name=name,
            type=type,
            image_urls=image_urls,
            url=res.url,
            cheapest_price=cheapest_price,
            in_stock=in_stock,
            vendors=vendors,
            rating=rating,
            specs=specs,
            reviews=reviews,
        )

    def parse_review(self, review: HTML, base_url: str) -> Review:
        # ... (không thay đổi)
        user_details = review.find(".userDetails", first=True)
        avatar_url = user_details.find("img", first=True).attrs["src"]
        if avatar_url.startswith("//"):
            avatar_url = "https:" + avatar_url
        else:
            avatar_url = base_url + avatar_url

        name_container = user_details.find(".userDetails__userName a", first=True)
        profile_url = base_url + name_container.attrs["href"]
        username = name_container.text

        user_data = user_details.find(".userDetails__userData", first=True)
        points = int(user_data.find("li:first-child", first=True).text.split(" ")[0])
        created_at = user_data.find("li:last-child", first=True).text

        review_name = review.find(".partReviews__name", first=True)
        stars = len(review_name.find(".product--rating .shape-star-full"))

        build_name = None
        build_url = None
        build_a = review_name.find("a", first=True)
        if build_a is not None:
            build_name = build_a.text
            build_url = base_url + build_a.attrs["href"]

        content = review.find(".partReviews__writeup", first=True).text

        return Review(
            author=User(username, avatar_url, profile_url),
            points=points,
            stars=stars,
            created_at=created_at,
            content=content,
            build_name=build_name,
            build_url=build_url,
        )

    def prepare_part_reviews_url(
        self,
        id_url: str,
        page: int = 1,
        rating: Optional[int] = None,
    ):
        base = self.prepare_part_url(id_url)
        if rating is None:
            return f"{base}{PART_REVIEWS_PATH}?page={page}"
        return f"{base}{PART_REVIEWS_PATH}?page={page}&rating={rating}"

    def parse_reviews(self, res: Response):
        # THAY ĐỔI: Tạo đối tượng HTML từ `res.text`
        html: HTML = HTML(html=res.text, url=res.url)
        base_url = "https://" + urllib.parse.urlparse(res.url).netloc
        reviews = []
        for review in html.find(".partReviews .partReviews__review"):
            reviews.append(self.parse_review(review, base_url))

        pagination = html.find("#module-pagination", first=True)

        try:
            current_page = int(pagination.find(".pagination--current", first=True).text)
            total_pages = int(pagination.find("li:last-child", first=True).text)
        except AttributeError:
            current_page = 0
            total_pages = 0

        return PartReviewsResult(
            reviews=reviews, page=current_page, total_pages=total_pages
        )

    def prepare_part_list_url(self, id_url: str, region: str = None) -> str:
        # ... (không thay đổi)
        match = PART_LIST_URL_RE.match(id_url)
        override_region = region
        if match is None:
            url = ID_RE.match(id_url)
            if url is None:
                raise ValueError("Invalid pcpartpicker part list URL or ID.")

            id_url = url.group(1)
            region = "us"
        else:
            region = "us" if match.group(2) is None else match.group(2)[:-1]
            id_url = match.group(3)

        if override_region is not None:
            region = override_region

        if id_url is None:
            raise ValueError("Invalid pcpartpicker part list URL or ID.")

        return self.__get_base_url(region) + PART_LIST_PATH + id_url

    def parse_part_list(self, res: Response) -> PartList:
        # THAY ĐỔI: Tạo đối tượng HTML từ `res.text`
        html: HTML = HTML(html=res.text, url=res.url)
        wrapper = html.find(".partlist__wrapper", first=True)
        part_list = html.find(".partlist", first=True)

        estimated_wattage = (
            wrapper.find(".partlist__keyMetric", first=True)
            .text.removeprefix("Estimated Wattage:")
            .strip()
        )

        # ... (phần còn lại của hàm không thay đổi, vì nó đã sử dụng `html` đã được tạo)
        # Parts
        parts = []
        for row in part_list.find("table tbody tr.tr__product"):
            type = row.find(".td__component", first=True).text.strip()

            image = row.find(".td__image img", first=True)
            image_urls = []
            if image is not None:
                image_urls = [image.attrs["src"]]

            name = "\n".join(
                filter(
                    lambda s: len(s) > 0,
                    (
                        row.find(".td__name", first=True)
                        .text.replace("From parametric selection:", "")
                        .strip()
                    ).split("\n"),
                )
            )
            part_link = row.find(".td__name a", first=True)
            url = None
            if part_link is not None:
                url = (
                    "https://"
                    + urllib.parse.urlparse(res.url).netloc
                    + part_link.attrs["href"]
                )

            base_price_raw = (
                row.find(".td__base", first=True).text.replace("Base", "").strip()
            )
            base_price_search = DECIMAL_RE.search(base_price_raw)
            base_price = (
                None
                if not base_price_search
                else base_price_search.group()
            )
            currency = (
                None if base_price is None else base_price_raw.replace(base_price, "")
            )

            vendors = []
            in_stock = False
            total_price = None

            if base_price is not None:
                promo_raw = row.find(".td__promo", first=True).text
                promo_search = DECIMAL_RE.search(promo_raw)
                promo = float(
                    0
                    if currency not in promo_raw or not promo_search
                    else promo_search.group()
                )

                shipping_raw = row.find(".td__shipping", first=True).text.strip()
                shipping_search = DECIMAL_RE.search(shipping_raw)
                shipping = float(
                    0
                    if "FREE" in shipping_raw
                    or shipping_raw == ""
                    or currency not in shipping_raw or not shipping_search
                    else shipping_search.group()
                )

                tax_raw = row.find(".td__tax", first=True).text.strip()
                tax_search = DECIMAL_RE.search(tax_raw)
                tax = float(
                    0
                    if tax_raw == "" or currency not in tax_raw or not tax_search
                    else tax_search.group()
                )
                
                total_price_search = DECIMAL_RE.search(row.find(".td__price", first=True).text)
                total_price = float(
                    total_price_search.group()
                ) if total_price_search else 0.0
                in_stock = True

                vendor = row.find(".td__where a", first=True)
                buy_url = vendor.attrs["href"]
                vendor_logo = vendor.find("img", first=True)
                vendor_name = vendor_logo.attrs["alt"]
                logo_url = "https:" + vendor_logo.attrs["src"]

                vendors = [
                    Vendor(
                        name=vendor_name,
                        logo_url=logo_url,
                        in_stock=in_stock,
                        price=Price(
                            None if base_price is None else float(base_price),
                            None if promo is None else -promo,
                            shipping,
                            tax,
                            total_price,
                            currency,
                        ),
                        buy_url=buy_url,
                    )
                ]
            else:
                total_price_raw = row.find(".td__price", first=True).text.strip()
                if (
                    "No Prices Available" not in total_price_raw
                    and total_price_raw != ""
                ):
                    total_price_search = DECIMAL_RE.search(total_price_raw)
                    if total_price_search:
                        total_price = total_price_search.group()
                        currency = (
                            total_price_raw.replace(total_price, "")
                            .replace("Price", "")
                            .strip()
                        )
                        total_price = float(total_price)

            parts.append(
                Part(
                    name,
                    type,
                    image_urls,
                    url,
                    (
                        Price(
                            base=float(base_price) if base_price else None,
                            discounts=0,
                            shipping=0,
                            tax=0,
                            total=total_price,
                            currency=currency,
                        )
                        if total_price is not None
                        else (
                            None
                            if vendors == []
                            else None if currency is None else vendors[0].price
                        )
                    ),
                    in_stock,
                    vendors=vendors,
                    rating=None,
                    specs=None,
                )
            )

        currency = None
        total_price = 0
        total = part_list.find(".tr__total--final .td__price", first=True)
        if total is not None:
            total_price_search = DECIMAL_RE.search(total.text)
            if total_price_search:
              total_price = total_price_search.group()
              currency = total.text.replace(total_price, "").strip()

        return PartList(
            parts=parts,
            url=res.url,
            estimated_wattage=estimated_wattage,
            total_price=float(total_price),
            currency=currency,
        )

    def prepare_search_url(self, query: str, page: int, region: Optional[str] = "us"):
        # ... (không thay đổi)
        return (
            self.__get_base_url("us" if region is None else region)
            + SEARCH_PATH
            + f"?q={urllib.parse.quote(query)}&page={page}"
        )

    def parse_part_search(self, res: Response) -> PartSearchResult:
        # THAY ĐỔI: Tạo đối tượng HTML từ `res.text`
        html: HTML = HTML(html=res.text, url=res.url)

        # ... (phần còn lại của hàm không thay đổi)
        # Case for which the search redirects to the product page
        page_title = html.find(".pageTitle", first=True)
        if not page_title or page_title.text != "Product Search":
            # Chuyển res tới parse_part, nhưng res giờ là requests.Response
            # nên parse_part đã được sửa để xử lý nó.
            return PartSearchResult(parts=[self.parse_part(res)], page=1, total_pages=1)

        results = []
        for result in html.find(".search-results__pageContent li"):
            image_url = (
                "https:"
                + result.find(".search_results--img img", first=True).attrs["src"]
            )
            link = result.find(".search_results--link a", first=True)

            url = (
                "https://" + urllib.parse.urlparse(res.url).netloc + link.attrs["href"]
            )
            name = link.text

            price = result.find(".search_results--price", first=True).text.strip()
            cheapest_price = None
            if price != "":
                total_search = DECIMAL_RE.search(price)
                if total_search:
                    total = total_search.group()
                    currency = price.replace(total, "").strip()
                    cheapest_price = Price(
                        base=None,
                        discounts=None,
                        shipping=None,
                        tax=None,
                        total=float(total),
                        currency=currency,
                    )

            type = None

            match "(".join(name.split("(")[:-1]).split(" ")[-4:-1]:
                case [*_, "Processor"]:
                    type = "CPU"
                case [_, "Fan", "Controller"]:
                    type = "Fan Controller"
                case [_, "Network", "Adapter"]:
                    type = "Wired Network Adapter"
                case [_, "Wi-Fi", "Adapter"]:
                    type = "Wireless Network Adapter"
                case [_, "Video", "Card"]:
                    type = "Video Card"
                case [_, "CPU", "Cooler"]:
                    type = "CPU Cooler"
                case [_, "Power", "Supply"]:
                    type = "Power Supply"
                case [_, "Thermal", "Paste"]:
                    type = "Thermal Compound"
                case [_, "Sound", "Card"]:
                    type = "Sound Card"
                case [_, "Fans", _] | [*_, "Fan"]:
                    type = "Case Fan"
                case ["External", _, _] | [_, "External", _]:
                    type = "External Storage"
                case [*_, "Writer"]:
                    type = "Optical Drive"
                case [*_, "Headset"] | [*_, "Headphones"]:
                    type = "Headphones"
                case ["Solid", "State", "Drive"] | [_, "Hard", "Drive"]:
                    type = "Storage"
                case [*_, a]:
                    type = a
            if "Windows" in name:
                type = "Operating System"

            results.append(
                Part(
                    name=name,
                    type=type,
                    image_urls=[image_url],
                    url=url,
                    cheapest_price=cheapest_price,
                    in_stock=cheapest_price is not None,
                    vendors=None,
                    rating=None,
                    specs=None,
                )
            )

        pagination = html.find("#module-pagination", first=True)

        try:
            current_page = int(pagination.find(".pagination--current", first=True).text)
            total_pages = int(pagination.find("li:last-child", first=True).text)
        except (AttributeError, ValueError):
            # Nếu chỉ có 1 trang, có thể không có pagination
            current_page = 1 if results else 0
            total_pages = 1 if results else 0

        return PartSearchResult(
            parts=results, page=current_page, total_pages=total_pages
        )

# Các hàm đã comment out không cần thay đổi