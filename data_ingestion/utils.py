import requests
import asyncio
from functools import partial

from logs import get_logger


logger = get_logger(__name__)


def http_get(url):
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            logger.info("Get HTTP response ok for %s", url)
            return response.json()
    except Exception as e:
        logger.exception(str(e))
        return {}


async def http_get_async(url):
    return await asyncio.to_thread(http_get, url)
