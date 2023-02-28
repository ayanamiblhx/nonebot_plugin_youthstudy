import json

from httpx import AsyncClient
from .utils import url_handle


async def get_pic():
    req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    async with AsyncClient(proxies={"all://": None}) as client:
        response = await url_handle(client, req_url)
        json_obj = json.loads(response.text)
        cover = json_obj['result']['cover']
        end = json_obj['result']['uri']
        if end.find("index.html") != -1:
            end = end.replace('index.html', 'images/end.jpg')
        elif end.find("m.html") != -1:
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
