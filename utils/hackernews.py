import requests

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
