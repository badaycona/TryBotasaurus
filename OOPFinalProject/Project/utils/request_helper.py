import httpx
import random
import asyncio
from utils.cloudflare_bypass import fetch_with_playwright
from utils.logger import get_logger

USER_AGENTS = [
    # Add more user agents for rotation
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
]

logger = get_logger('request_helper')

async def fetch_with_bypass(url, max_retries=3, use_playwright_on_fail=True):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Referer': 'https://www.google.com/',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 403 and use_playwright_on_fail:
                    logger.warning(f'403 detected, switching to Playwright for {url}')
                    return await fetch_with_playwright(url, user_agent=headers['User-Agent'])
        except Exception as e:
            logger.error(f'Error fetching {url}: {e}')
        await asyncio.sleep(2 ** attempt)
    logger.error(f'Failed to fetch {url} after {max_retries} attempts')
    return None
