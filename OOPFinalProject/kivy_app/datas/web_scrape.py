from botasaurus.browser import browser, Driver
from bs4 import BeautifulSoup

@browser()
def scrape_website_html(driver : Driver, link: str):
    """
    Hàm này truy cập một URL, lấy toàn bộ nội dung HTML,
    và lưu nó vào một file.
    """

    print(f"Đang truy cập vào URL: {link}")
    driver.get(link, bypass_cloudflare=True)

    html_content = driver.page_html
    print("Đã lấy thành công nội dung HTML.")

    with open("temp_content.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Đã lưu HTML vào file 'temp_content.html'")

    return html_content

if __name__ == "__main__":
    scrape_website_html("https://quotes.toscrape.com/")