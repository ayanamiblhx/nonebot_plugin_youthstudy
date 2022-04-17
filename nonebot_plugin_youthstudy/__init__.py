import time
import nonebot
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Event
from .getdata import get_answer
from nonebot.log import logger
from datetime import datetime
from .config import Config

global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())

if hasattr(plugin_config, 'qq_friends') and hasattr(plugin_config, 'qq_groups'):
    nonebot.logger.success("plugin_config:{}".format(plugin_config))
else:
    nonebot.logger.critical("plugin_config:{}".format(plugin_config))
    raise Exception("leetcode config error, please check env file")

college_study = on_command('青年大学习', aliases={'大学习'}, priority=5)

from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler

# 每周一10:00开始检测是否更新，每3分检测一次，觉得检测间隔太久，请手动修改time.sleep()，获取到答案后终止检测。
@scheduler.scheduled_job('cron', day_of_week='0', hour=10, minute=0)
async def remind():
        try:
            for i in range(10000):
                img = await get_answer()
                if img is None or img == '未找到答案':
                    time.sleep(180)
                else:
                    message = [
                        {
                            "type": "text",
                            "data": {
                                "text": '本周的青年大学习开始喽！'
                            }
                        },
                        {
                            "type": "image",
                            "data": {
                                "file": img
                            }
                        }
                    ]
                    # 给配置的列表里的qq好友发通知
                    for qq in plugin_config.qq_friends:
                        await nonebot.get_bot().send_private_msg(user_id=qq, message=message)
                        time.sleep(1)
                        # 给群发送通知
                    for qq_group in plugin_config.qq_groups:
                        await nonebot.get_bot().send_group_msg(group_id=qq_group,
                                                               message="[CQ:at,qq={}]{}".format("all", message))
                        time.sleep(1)
                    break
        except Exception as e:
            with open('./log.txt', 'a+', encoding='utf-8') as f:
                f.write(str(e))
            time.sleep(30)


@college_study.handle()
async def _(bot: Bot, event: Event, state: T_State):
    try:
        img = await get_answer()
        if img is None:
            await college_study.send("本周暂未更新青年大学习", at_sender=True)
        elif img == "未找到答案":
            await college_study.send("未找到答案", at_sender=True)
        else:
            await college_study.send(MessageSegment.image(img), at_sender=True)
    except Exception as e:
        await college_study.send(f"出错了，错误信息：{e}", at_sender=True)
        logger.error(f"{datetime.now()}: 错误信息：{e}")
