import requests
from bs4 import BeautifulSoup
import httpx
import asyncio

def crawl(url: str):
    """Fetches and parses the content of a URL."""
    if not url:
        return ""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator=' ', strip=True)
    except requests.RequestException as e:
        print(f"Error crawling {url}: {e}")
        return ""

async def crawl_async(url: str, semaphore: asyncio.Semaphore = None):
    """Fetches and parses the content of a URL asynchronously."""
    if not url:
        return ""
    
    async def _crawl():
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            return soup.get_text(separator=' ', strip=True)
        except httpx.HTTPError as e:
            print(f"Error crawling {url}: {e}")
            return ""

    if semaphore:
        async with semaphore:
            return await _crawl()
    else:
        return await _crawl()