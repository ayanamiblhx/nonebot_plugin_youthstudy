import asyncio
import re
from datetime import datetime

import nonebot
from nonebot import require
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Event, FriendRequestEvent
from nonebot.log import logger
from nonebot.plugin import on_regex, on_request

from .dao import UserDao, GroupDao
from .file_tool import FileTool
from .get_src import get_pic
from .getdata import get_answer
from .utils import YouthStudyEnum

scheduler = require('nonebot_plugin_apscheduler').scheduler
FileTool()


@scheduler.scheduled_job('cron', day_of_week='0', hour=10, minute=0, id='push_job')
async def _():
    logger.info("开始获取大学习答案")
    iterations = 0
    while True:
        try:
            img = await get_answer()
        except Exception as e:
            logger.error(e)
            await study_send_msg(f"自动获取答案出错，错误信息{e}")
        if img is None or img == '未找到答案':
            logger.info(f"{img}")
            logger.info(f"第{iterations}次循环")
            await asyncio.sleep(YouthStudyEnum.SLEEP_TIME)
            iterations += 1
        else:
            content = await get_pic()
            title = content['title']
            start_time = content['start_time']
            cover = content['cover']
            end = content['end']
            message = [
                {
                    "type": "text",
                    "data": {
                        "text": '本周的青年大学习开始喽！\n' +
                                title + '\n开始时间：' + start_time +
                                '\n答案见图二、完成截图见图三\nPs:如果学校会查后台记录，\n'
                                '请前往相应平台观看1分钟，\n确保在后台留下观看记录！！！\n' +
                                '你也可以把链接复制到微信进行截图以获取带手机状态栏的完成截图\nhttps://qndxx.scubot.live/\n'
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": cover
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": img
                    }
                },
                {
                    "type": "image",
                    "data": {
                        "file": end
                    }
                }
            ]
            await study_send_msg(message=message)
            break
        if iterations >= YouthStudyEnum.MAX_ITERATIONS:
            message_notfound = [
                {
                    "type": "text",
                    "data": {
                        "text": '本周没有大学习哦！'
                    }
                }
            ]
            await study_send_msg(message=message_notfound)
            break


async def study_send_msg(message):
    for user in UserDao().get_push_user():
        await nonebot.get_bot().send_private_msg(user_id=user, message=message)
        await asyncio.sleep(1)
    for group in GroupDao().get_push_group():
        await nonebot.get_bot().send_group_msg(group_id=group,
                                               message=message)
        await asyncio.sleep(1)


youth_study = on_regex('^青年大学习$|^大学习$')


@youth_study.handle()
async def _():
    try:
        img = await get_answer()
        if img is None:
            await youth_study.send("本周暂未更新青年大学习", at_sender=True)
        elif img == "未找到答案":
            await youth_study.send("未找到答案", at_sender=True)
        else:
            await youth_study.send(MessageSegment.image(img), at_sender=True)
    except Exception as e:
        await youth_study.send(f"出错了，错误信息：{e}", at_sender=True)
        logger.error(f"{datetime.now()}: 错误信息：{e}")


complete_scr = on_regex('^大学习截图$|^完成截图$')


@complete_scr.handle()
async def _(event: Event):
    try:
        msg = event.get_plaintext()
        content = await get_pic()
        scr = content['cover']
        end = content['end']
        if scr is None:
            await complete_scr.send("本周暂未更新青年大学习", at_sender=True)
        else:
            if msg == "大学习截图":
                await complete_scr.send(MessageSegment.image(scr), at_sender=True)
            elif msg == "完成截图":
                text = '你也可以把链接复制到微信进行截图以获取带手机状态栏的完成截图\nhttps://qndxx.scubot.live/\n'
                await complete_scr.send(MessageSegment.image(end) + MessageSegment.text(text), at_sender=True)
    except Exception as e:
        await complete_scr.send(f"出错了，错误信息：{e}", at_sender=True)
        logger.error(f"{datetime.now()}: 错误信息：{e}")


study_push = on_regex(r"^开启大学习推送$|^关闭大学习推送$")


@study_push.handle()
async def _(event: Event):
    msg_text = event.get_plaintext()
    user_id = event.get_user_id()
    group_id = 0 if not hasattr(event, 'group_id') else event.group_id
    if msg_text == "开启大学习推送":
        if group_id != 0:
            if user_id in FileTool().super_users:
                GroupDao().set_or_update_push(group_id, 1)
                await study_push.send(f"群{group_id}开启大学习推送成功", at_sender=True)
            else:
                await study_push.send("您没有权限使用此功能", at_sender=True)
        else:
            UserDao().set_or_update_push(user_id, 1)
            await study_push.send(f"用户{user_id}开启大学习推送成功", at_sender=True)
    elif msg_text == "关闭大学习推送":
        if group_id != 0:
            if user_id in FileTool().super_users:
                GroupDao().set_or_update_push(group_id, 0)
                await study_push.send(f"群{group_id}关闭大学习推送成功", at_sender=True)
            else:
                await study_push.send("您没有权限使用此功能", at_sender=True)
        else:
            UserDao().set_or_update_push(user_id, 0)
            await study_push.send(f"用户{user_id}关闭大学习推送成功", at_sender=True)


global_push = on_regex(r"^开启大学习全局推送$|^关闭大学习全局推送$")


@global_push.handle()
async def _(event: Event):
    msg = event.get_plaintext()
    if event.get_user_id() in FileTool().super_users:
        if msg == "开启大学习全局推送":
            scheduler.resume_job('push_job')
            await global_push.send(f"开启大学习全局推送成功", at_sender=True)
        elif msg == "关闭大学习全局推送":
            scheduler.pause_job('push_job')
            await global_push.send(f"关闭大学习全局推送成功", at_sender=True)
    else:
        await global_push.send("您没有权限使用此功能", at_sender=True)


push_list = on_regex(r"^查询大学习推送群列表$|^查询大学习推送用户列表$")


@push_list.handle()
async def _(event: Event):
    msg = event.get_plaintext()
    if event.get_user_id() in FileTool().super_users:
        groups = GroupDao().get_push_group()
        users = UserDao().get_push_user()
        if msg == "查询大学习推送群列表":
            if groups.__len__() == 0:
                await push_list.send("暂无群推送列表", at_sender=True)
            else:
                msg = "推送群列表："
                for group in groups:
                    msg += f"\n群号: {group}"
                await push_list.send(msg, at_sender=True)
        elif msg == "查询大学习推送用户列表":
            if users.__len__() == 0:
                await push_list.send("暂无用户推送列表", at_sender=True)
            else:
                msg = "推送用户列表："
                for user in users:
                    msg += f"\nqq: {user}"
                await push_list.send(msg, at_sender=True)
    else:
        await push_list.send("您没有权限使用此功能", at_sender=True)


async def friend_request(event: Event):
    return event.__class__.__name__ == "FriendRequestEvent"


friend_req = on_request(rule=friend_request)


@friend_req.handle()
async def friend_req(event: FriendRequestEvent, bot: Bot):
    try:
        comment = event.comment
        flag = event.flag
        user_id = event.user_id
        if UserDao().get_friend_req(user_id).__len__() > 0 \
                and flag == UserDao().get_friend_req(user_id)[0]["flag"]:
            return
        time = datetime.fromtimestamp(event.time).strftime('%Y年%m月%d日 %H时%M分%S秒')
        UserDao().set_or_update_friend_req(user_id, flag)
        for superuser in FileTool().super_users:
            await bot.send_msg(user_id=superuser,
                               message=f"QQ：{user_id}请求添加机器人为好友!\n请求添加时间：{time}\n验证信息为：{comment}")
    except Exception as e:
        logger.error(e)
        for superuser in FileTool().super_users:
            await bot.send_msg(user_id=superuser, message=f"添加好友请求失败,错误信息{e}")


friend_req_handle = on_regex(r"^同意所有好友请求$|^拒绝所有好友请求$|^同意[1-9][0-9]{4,10}$|^拒绝[1-9][0-9]{4,10}$")


@friend_req_handle.handle()
async def _(event: Event, bot: Bot):
    msg = event.get_plaintext()
    if event.get_user_id() in FileTool().super_users:
        if msg == "同意所有好友请求":
            for req in UserDao().get_friend_req():
                await bot.set_friend_add_request(flag=req["flag"], approve=True)
            await friend_req_handle.send("同意所有好友请求成功", at_sender=True)
        elif msg == "拒绝所有好友请求":
            for req in UserDao().get_friend_req():
                await bot.set_friend_add_request(flag=req["flag"], approve=False)
            await friend_req_handle.send("拒绝所有好友请求成功", at_sender=True)
        elif bool(re.match(r"^同意[1-9]\d{4,10}$", msg)):
            user_id = re.sub(r'\D+', '', msg)
            req = UserDao().get_friend_req(user_id)
            if req.__len__() == 1:
                await bot.set_friend_add_request(flag=req[0]["flag"], approve=True)
                await friend_req_handle.send(f"同意{user_id}好友请求成功", at_sender=True)
            else:
                await friend_req_handle.send(f"没有来自{user_id}的好友请求", at_sender=True)
        elif bool(re.match(r"^拒绝[1-9]\d{4,10}$", msg)):
            user_id = re.sub(r'\D+', '', msg)
            req = UserDao().get_friend_req(user_id)
            if req.__len__() == 1:
                await bot.set_friend_add_request(flag=req[0]["flag"], approve=False)
                await friend_req_handle.send(f"拒绝{user_id}好友请求成功", at_sender=True)
            else:
                await friend_req_handle.send(f"没有来自{user_id}的好友请求", at_sender=True)
    else:
        await friend_req_handle.send("您没有权限使用此功能", at_sender=True)


help_list = on_regex('^大学习帮助$')


@help_list.handle()
async def _():
    import pkg_resources
    try:
        _dist: pkg_resources.Distribution = pkg_resources.get_distribution("nonebot_plugin_youthstudy")
        _help = f'大学习版本：{_dist.version}\n' \
                '大学习功能指令\n' \
                '主人专用:\n' \
                '1、开启(关闭)大学习推送(群聊使用)\n2、查询大学习推送用户(群)列表\n' \
                '4、开启(关闭)大学习全局推送\n5、处理好友请求：同意(拒绝)QQ号或同意(拒绝)所有好友请求\n' + \
                '全员可用功能:\n' \
                '1、开启(关闭)大学习推送(私聊使用)\n2、青年大学习或大学习\n3、大学习截图或完成截图\n4、大学习帮助 '

        await help_list.send(_help, at_sender=True)
    except Exception as e:
        logger.error(e)
        await help_list.send(f'出错了，错误信息{e}', at_sender=True)
