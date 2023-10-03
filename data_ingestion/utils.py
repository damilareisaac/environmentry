import requests
import asyncio
from functools import partial

from logs import get_logger


logger = partial(get_logger, __name__)


def http_get(url):
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            logger(to_console=True).info("Get HTTP response ok for %s", url)
            return response.json()
    except Exception as e:
        logger(to_console=True).exception(str(e))
        return {}


async def http_get_async(url):
    return await asyncio.to_thread(http_get, url)
