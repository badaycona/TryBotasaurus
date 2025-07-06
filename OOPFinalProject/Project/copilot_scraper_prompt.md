# GitHub Copilot Prompt for Full Python Web Scraping Project

## 📌 Goal:
Create a complete Python-based web scraping project that extracts data from **pcpartpicker.com** for the following computer parts:

- CPU
- GPU
- RAM
- PSU
- Motherboard

## 📦 Output:
All scraped data should be saved in clean, structured **JSON** files, organized by part type. (e.g., `cpus.json`, `gpus.json`, etc.)

## 🚧 Requirements:

1. **Cloudflare Bypass & Anti-Bot Handling**
    - Automatically handle Cloudflare challenge pages.
    - Bypass HTTP 403 errors (IP bans, bot detection).
    - Mimic real user behavior (headers, delays, user agents, referers, etc.).
    - If needed, integrate headless browser (e.g. Playwright or Selenium with stealth mode).

2. **Code Structure (Modular)**
    Break the code into well-separated modules:

    - `main.py`: Entry point.
    - `scraper/`
        - `__init__.py`
        - `cpu_scraper.py`
        - `gpu_scraper.py`
        - `ram_scraper.py`
        - `psu_scraper.py`
        - `motherboard_scraper.py`
    - `utils/`
        - `cloudflare_bypass.py`
        - `request_helper.py`
        - `json_writer.py`
        - `logger.py`

3. **Best Practices**
    - Use async requests where possible (e.g., `httpx`, `aiohttp`) to speed up scraping.
    - Include retry logic with exponential backoff.
    - Use rotating proxies and user agents.
    - Respect robots.txt and scraping ethics.
    - Modular, clean, commented, production-ready code.

4. **Installation and Usage**
    - Provide a `requirements.txt` file.
    - Include a `README.md` that documents:
        - How to install dependencies
        - How to run the project
        - How the code is structured
        - Where the JSON data will be saved

## 🤖 Task:
Write the entire project code from scratch and organize it into multiple files and folders as described above. Ensure all necessary parts for running the project successfully are included.

---

## 🔧 Extra (Optional but Recommended):
- Automatically detect if a page fails (403, timeout, etc.) and reattempt scraping.
- Add logging for debugging and tracking scraped items.
- Allow selection of categories to scrape via CLI (e.g., `--cpu`, `--gpu`, etc.).
- Add caching to avoid repeated scraping of the same URLs.

---

## ✅ Acceptance Criteria:
- Scraper successfully extracts relevant info (name, price, specs, etc.) for each component type.
- JSON files are well-structured and complete.
- Code runs successfully end-to-end.
- Cloudflare or bot detection does not block the scraper.
- Clear README with setup and usage instructions.

