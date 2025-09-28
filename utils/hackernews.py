import requests
import httpx
import asyncio

HN_API_BASE_URL = "https://hacker-news.firebaseio.com/v0"

def get_item(item_id: int):
    """Fetches an item from the Hacker News API."""
    try:
        response = requests.get(f"{HN_API_BASE_URL}/item/{item_id}.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching item {item_id}: {e}")
        return None

async def get_item_async(item_id: int, semaphore: asyncio.Semaphore = None):
    """Fetches an item from the Hacker News API asynchronously."""
    url = f"{HN_API_BASE_URL}/item/{item_id}.json"
    if semaphore:
        async with semaphore:
            return await _fetch_url(url)
    return await _fetch_url(url)

def get_top_story_ids(limit: int = 20):
    """Fetches top story IDs from the Hacker News API."""
    try:
        response = requests.get(f"{HN_API_BASE_URL}/topstories.json")
        response.raise_for_status()
        return response.json()[:limit]
    except requests.RequestException as e:
        print(f"Error fetching top stories: {e}")
        return []

def get_comments(item: dict, limit: int = 10):
    """Fetches comments for a given story item."""
    if not item or 'kids' not in item:
        return []

    comment_ids = item['kids'][:limit]
    comments = []
    for comment_id in comment_ids:
        comment = get_item(comment_id)
        if comment and not comment.get('deleted') and not comment.get('dead'):
            comments.append(comment)
    return comments

async def get_comments_async(item: dict, limit: int = 10, semaphore: asyncio.Semaphore = None):
    """Fetches comments for a given story item asynchronously."""
    if not item or 'kids' not in item:
        return []

    comment_ids = item['kids'][:limit]
    
    tasks = [get_item_async(comment_id, semaphore) for comment_id in comment_ids]
    comments = await asyncio.gather(*tasks)
    
    return [comment for comment in comments if comment and not comment.get('deleted') and not comment.get('dead')]

async def _fetch_url(url: str):
    """Helper to fetch and parse a URL with a new client."""
    async with httpx.AsyncClient() as client:
        try:
            await asyncio.sleep(0.1) # polite delay
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Error fetching {url}: {e}")
            return None
