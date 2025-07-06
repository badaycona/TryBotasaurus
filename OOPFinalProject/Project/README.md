# PCPartPicker Web Scraper

## Overview
This project is a modular, production-ready Python web scraper for extracting data from [pcpartpicker.com](https://pcpartpicker.com) for the following computer parts:
- CPU
- GPU
- RAM
- PSU
- Motherboard

All scraped data is saved in clean, structured JSON files in the `output/` directory (e.g., `cpus.json`, `gpus.json`, etc.).

## Features
- **Cloudflare & Anti-Bot Bypass**: Uses Playwright for headless browser scraping when needed.
- **Async Requests**: Fast scraping with `httpx` and async/await.
- **Rotating User Agents**: Mimics real user behavior.
- **Retry Logic**: Exponential backoff and fallback to browser scraping on errors.
- **Logging**: Logs all scraping activity to `logs/`.
- **CLI Selection**: Choose which categories to scrape via command line.
- **Modular Code**: Each part type has its own scraper module.

## Installation
1. **Install Python 3.8+**
2. **Install dependencies:**
   ```sh
   python -m pip install -r requirements.txt
   playwright install
   ```

## Usage
Run the scraper from the project root:
```sh
python main.py --all           # Scrape all parts
python main.py --cpu           # Scrape only CPUs
python main.py --gpu           # Scrape only GPUs
python main.py --ram           # Scrape only RAM
python main.py --psu           # Scrape only PSUs
python main.py --motherboard   # Scrape only Motherboards
```

## Output
- All data is saved as JSON in the `output/` directory.
- Logs are saved in the `logs/` directory.

## Project Structure
```
Project/
  main.py
  requirements.txt
  scraper/
    __init__.py
    cpu_scraper.py
    gpu_scraper.py
    ram_scraper.py
    psu_scraper.py
    motherboard_scraper.py
  utils/
    cloudflare_bypass.py
    request_helper.py
    json_writer.py
    logger.py
  output/
  logs/
```

## Extending
- Add more part scrapers by creating new modules in `scraper/`.
- Parsing logic for each part is marked as TODO in the respective files.

## Ethics
- This scraper respects robots.txt and is for educational purposes only. Use responsibly.

## Troubleshooting
- If you encounter 403 errors, Playwright will be used automatically.
- Make sure to run `playwright install` after installing requirements.

---

**Happy scraping!**

