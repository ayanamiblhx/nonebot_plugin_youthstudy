import time
from httpx import AsyncClient
from datetime import datetime
import json
from bs4 import BeautifulSoup
from .convert_pic import convert_pic


async def get_update():
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53"
    }
    req_url = "https://qczj.h5yunban.com/qczj-youth-learning/cgi-bin/common-api/course/current"
    async with AsyncClient(proxies={"all://": None}) as client:
        try:
            res = await client.get(req_url, headers=head, timeout=10)
            if res.status_code == 200:
                data = json.loads(res.text)
                return data
            else:
                raise f"请求失败{res.status_code}"
        except Exception as e:
            raise e


async def parse_html(uri):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53"
    }
    start_div = '<div class="section0 topindex">'
    end_div = '<!-- <script type="text/javascript" src="js/index.js"></script>'
    tmp = []
    answer_attrs = {"required": [], "optional": []}
    option = "ABCDEF"
    template = "{num}. {check}"
    async with AsyncClient(proxies={"all://": None}) as client:
        try:
            res = await client.get(uri, headers=head, timeout=10)
            if res.status_code == 200:
                start = res.text.find(start_div)
                end = res.text.find(end_div)
                if start == -1 or end == -1:
                    return []
                else:
                    soup = BeautifulSoup(res.text[start:end], 'lxml')
                    for div in soup.find("body"):
                        if div == "\n":
                            continue
                        answer = []
                        if div.name == "div":
                            for i in div.find_all("div"):
                                check = i.get("data-a")
                                if check is not None:
                                    answer.append(check)

                            if len(answer) > 4:
                                answer = answer[:int(len(answer) / 2)]
                            tmp.append(answer)
                    req_end = 0
                    flag = {"location": 0, "result": True}
                    for i, v in enumerate(tmp):
                        if len(v) == 0:
                            req_end = i + 1
                        elif flag["result"]:
                            flag["result"] = False
                            flag["location"] = i
                    for i, v in enumerate(tmp):
                        if flag["location"] < req_end and req_end - 1 > i >= flag["location"]:
                            field = "required"
                            answer_attrs[field].append(v)
                        elif flag["location"] == req_end and i >= req_end:
                            field = "optional"
                            answer_attrs[field].append(v)
                        elif flag["location"] < req_end <= i:
                            field = "optional"
                            answer_attrs[field].append(v)

                    # process
                    output = []
                    if len(answer_attrs["required"]) > 0:
                        output.append("本期答案\n")
                        for i, v in enumerate(answer_attrs["required"]):
                            checks = ""
                            for j, v2 in enumerate(v):
                                if v2 == "1":
                                    checks += option[j]
                            output.append(template.format(num=i + 1, check=checks) + "\n")
                    if len(answer_attrs["optional"]) != 0:
                        output.append("课外习题\n")
                        for i, v in enumerate(answer_attrs["optional"]):
                            checks = ""
                            for j, v2 in enumerate(v):
                                if v2 == "1":
                                    checks += option[j]
                            output.append(template.format(num=i + 1, check=checks) + "\n")
                    result = [output[0]]
                    for i, v in enumerate(output):
                        if i % 13 != 0 and i != 0:
                            result[int(i / 13)] += v
                        elif i % 13 == 0 and i != 0:
                            result.append(v)
                    return result
            else:
                raise f"请求失败{res.status_code}"
        except Exception as e:
            raise e


async def get_answer():
    update = await get_update()
    if not update:
        return "未找到答案"
    now = datetime.now().date()
    start_time = datetime.strptime(update["result"]["startTime"], "%Y-%m-%d %H:%M:%S").date()
    days = (now - start_time).days
    if days < 7:
        end_time = time.strptime(update["result"]["endTime"], "%Y-%m-%d %H:%M:%S")
        end_time = '结束日期: ' + time.strftime("%m{m}%d{d}%H{H}%M{M}", end_time).format(m='月', d='日', H='时', M='分')
        title = "青年大学习" + update["result"]["type"]
        period = update["result"]["title"]
        answer = await parse_html(update["result"]["uri"])
    else:
        return None
    text = {"title": title, "period": period, "answer": answer, "end_time": end_time}
    img = await convert_pic(text)
    return img
