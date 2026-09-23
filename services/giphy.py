import os
import random
import asyncio
import aiohttp

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
GIPHY_SEARCH_URL = "https://api.giphy.com/v1/gifs/search"
GIFS_PER_TERM = 15

GIF_SEARCH_TERMS = {
    "correct": ["victory dance", "celebration", "you did it"],
    "wrong": ["oh no", "facepalm", "fail"],
    "timeout": ["waiting", "time is up", "clock ticking"],
    "thinking": ["confused", "thinking", "hmm"],
}

gif_cache = {status: [] for status in GIF_SEARCH_TERMS}

async def fetch_gifs(session, term):
    params = {
        "api_key": GIPHY_API_KEY,
        "q": term,
        "limit": GIFS_PER_TERM,
        "rating": "g",
    }
    try:
        async with session.get(GIPHY_SEARCH_URL, params=params) as response:
            if response.status != 200:
                print(f"Giphy error {response.status} searching '{term}'")
                return []
            data = await response.json()
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        print(f"Could not fetch Giphy for '{term}': {error}")
        return []

    urls = []
    for item in data.get("data", []):
        image = item.get("images", {}).get("downsized")
        if image and image.get("url"):
            urls.append(image["url"])
    return urls

async def update_gif_cache():
    if not GIPHY_API_KEY:
        return

    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for status, terms in GIF_SEARCH_TERMS.items():
            results = await asyncio.gather(*(fetch_gifs(session, t) for t in terms))
            urls = [url for group in results for url in group]
            if urls:
                gif_cache[status] = urls

def get_gif(status):
    urls = gif_cache.get(status)
    return random.choice(urls) if urls else None