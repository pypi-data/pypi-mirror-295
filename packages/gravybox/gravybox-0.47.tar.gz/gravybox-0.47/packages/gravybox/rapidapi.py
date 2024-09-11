import os

from gravybox.betterstack import collect_logger
from gravybox.exceptions import BadStatusCode
from gravybox.requests import AsyncRequestManager

logger = collect_logger()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


async def query_rapidapi(url, host, query, extra_headers=None):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": host
    }
    if extra_headers is not None:
        headers |= extra_headers
    response = await AsyncRequestManager.client().get(url, headers=headers, params=query)
    if response.status_code == 200:
        return response.json()
    else:
        raise BadStatusCode(response)
