import requests
import asyncio


def http_get(url):
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return {}


async def http_get_async(url):
    return await asyncio.to_thread(http_get, url)
