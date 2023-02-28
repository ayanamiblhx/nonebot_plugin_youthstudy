from enum import IntEnum

from httpx import TimeoutException, HTTPError
from nonebot import logger

class YouthStudyEnum(IntEnum):
    """
    SLEEP_TIME: 睡眠时间\n
    ITERATIONS: 迭代次数\n
    """
    SLEEP_TIME = 180
    MAX_ITERATIONS = 200


async def url_handle(client, uri):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53"
    }
    loops = 0
    while True:
        loops += 1
        if loops > 10:
            api_exception = '获取api失败次数过多，请检查网络链接'
            logger.error(api_exception)
            raise Exception(api_exception)
        try:
            res = await client.get(uri, headers=head, timeout=10)
            if res.status_code == 200:
                break
        except TimeoutException as e:
            logger.error(f"获取api内容超时{type(e)}")
        except HTTPError as e:
            logger.error(f"网络错误：{type(e)}")
            raise e
    return res

