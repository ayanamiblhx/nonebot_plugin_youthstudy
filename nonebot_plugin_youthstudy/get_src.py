import json

from httpx import AsyncClient
from nonebot.log import logger


async def get_pic():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41",
    }
    req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    try:
        async with AsyncClient(headers=headers, proxies={"all://": None}) as client:
            response = await client.get(req_url)
            response.encoding = response.apparent_encoding
            json_obj = json.loads(response.text)
            cover = json_obj['result']['cover']
            try:
                end = json_obj['result']['uri'].replace('index.html', 'images/end.jpg')
            except Exception as e:
                logger.error(e)
                end = json_obj['result']['uri'][:-6] + 'images/end.jpg'
            start_time = json_obj['result']['startTime']
            title = json_obj['result']['title']
            data = {
                'cover': cover,
                'end': end,
                'start_time': start_time,
                'title': title
            }
            return data
    except Exception as e:
        logger.error(e)
        raise e
