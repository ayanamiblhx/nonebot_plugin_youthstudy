import requests
import json

async def get_pic():
    headears = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    try:
        response = requests.get(req_url,headears)
        response.encoding = response.apparent_encoding
        json_obj = json.loads(response.text)
        cover = json_obj['result']['cover']
        try:
            url = json_obj['result']['uri'].replace('m.html', 'images/end.jpg')
        except:
            url = json_obj['result']['uri'][:-6] + 'images/end.jpg'
        starttime = json_obj['result']['startTime']
        title = json_obj['result']['title']
        return [title,starttime,cover,url]
    except:
        return ['标题获取失败！','开始时间获取失败！','','']
