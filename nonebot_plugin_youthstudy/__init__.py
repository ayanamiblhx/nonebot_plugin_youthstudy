from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from .getdata import get_answer
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.log import logger
from datetime import datetime

__plugin_name__ = "青年大学习"
college_study = on_command('青年大学习', aliases={'大学习'}, priority=5)


@college_study.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
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
