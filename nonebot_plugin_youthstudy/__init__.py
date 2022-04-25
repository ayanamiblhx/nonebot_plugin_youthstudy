import json
import time
import nonebot
import pathlib
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_request
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Event, FriendRequestEvent
from nonebot.log import logger
from .getdata import get_answer
from datetime import datetime
from .get_src import get_pic
from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler
# 获取超管id
super_id = nonebot.get_driver().config.superusers


# 每周一10:00开始检测是否更新，每3分检测一次，觉得检测间隔太久，请手动修改time.sleep()，获取到答案后终止检测。
@scheduler.scheduled_job('cron', day_of_week='0', hour=10, minute=0, id='a')
async def remind():
    try:
        num = 0
        for i in range(960):
            img = await get_answer()
            if img is None or img == '未找到答案':
                time.sleep(180)
                num += 1
            else:
                content = await get_pic()
                title = content[0]
                starttime = content[1]
                cover = content[2]
                end_url = content[3]
                message = [
                    {
                        "type": "text",
                        "data": {
                            "text": '本周的青年大学习开始喽！\n' + title + '\n开始时间：' + starttime + '\n答案见图二、完成截图见图三\nPs:如果学校会查后台记录，\n请前往相应平台观看1分钟，\n确保在后台留下观看记录！！！ '
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
                            "file": end_url
                        }
                    }
                ]
                # 读取需要推送的群和好友
                with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                qq_friend_list = obj['qq_friend_list']
                qq_group_list = obj['qq_group_list']
                # 给配置的列表里的qq好友发通知
                for qq in qq_friend_list:
                    await nonebot.get_bot().send_private_msg(user_id=qq, message=message)
                    time.sleep(1)
                    # 给群发送通知
                for qq_group in qq_group_list:
                    await nonebot.get_bot().send_group_msg(group_id=qq_group,
                                                           message="[CQ:at,qq={}]{}".format("all", message))
                    time.sleep(1)
                break
            if num >= 200:
                message1 = [
                    {
                        "type": "text",
                        "data": {
                            "text": '本周没有大学习哦！'
                        }
                    }
                ]
                # 读取需要推送的群和好友
                with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                qq_friend_list = obj['qq_friend_list']
                qq_group_list = obj['qq_group_list']
                # 给配置的列表里的qq好友发通知
                for qq in qq_friend_list:
                    await nonebot.get_bot().send_private_msg(user_id=qq, message=message1)
                    time.sleep(1)
                    # 给群发送通知
                for qq_group in qq_group_list:
                    await nonebot.get_bot().send_group_msg(group_id=qq_group,
                                                           message="[CQ:at,qq={}]{}".format("all", message1))
                    time.sleep(1)

                break
    except Exception as e:
        for qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(qq), message=f'机器人出错了\n错误信息：{e}')


# 以下指令为机器人主人指令
# 机器人主人使用，用于关闭所有大学习自动更新推送
close_time_task = on_command('全局关闭大学习推送', aliases={'全局关闭推送'}, permission=SUPERUSER)


@close_time_task.handle()
async def close_time_task(state: T_State, event: Event):
    try:
        scheduler.pause_job(job_id='a')
        await nonebot.get_bot().send(message="已全局关闭青年大学习自动检查更新推送。", at_sender=True, event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'出错了!\n错误日志:{e}', at_sender=True, event=event)


# 机器人主人使用，用于开启所有大学习自动更新推送
recover_time_task = on_command('全局开启大学习推送', aliases={'全局开启推送'}, permission=SUPERUSER)


@recover_time_task.handle()
async def recover_time_task(state: T_State, event: Event):
    try:
        scheduler.resume_job(job_id='a')
        await nonebot.get_bot().send(message='已全局开启青年大学习自动检查更新推送。', at_sender=True, event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'出错了!\n错误日志:{e}', at_sender=True, event=event)


# 机器人主人使用，用于添加推送好友
add_friend_list = on_command('添加推送好友', permission=SUPERUSER)


@add_friend_list.handle()
async def add_friend_list(event: Event):
    try:
        # 读取需要推送的好友
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_friend_list = obj['qq_friend_list']
        user_id = int(str(event.get_user_id()))
        add_qq = int(str(event.get_message()).split('#')[-1])
        if add_qq not in qq_friend_list:
            await nonebot.get_bot().send(user_id=user_id, message=f'已将好友：{add_qq}加入推送列表', event=event)
            qq_friend_list.append(add_qq)
            obj['qq_friend_list'] = qq_friend_list
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
        else:
            await nonebot.get_bot().send(user_id=user_id, message=f'加入失败！\n好友：{add_qq}已经在推送列表中了', event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'出错了!\n错误日志:{e}', at_sender=True, event=event)


# 机器人主人使用，用于删除推送好友
del_friend_list = on_command('删除推送好友', permission=SUPERUSER)


@del_friend_list.handle()
async def del_friend_list(event: Event):
    try:
        # 读取需要推送的好友
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_friend_list = obj['qq_friend_list']
        user_id = int(str(event.get_user_id()))
        del_qq = int(str(event.get_message()).split('#')[-1])
        if del_qq not in qq_friend_list:
            await nonebot.get_bot().send(user_id=user_id, message=f'删除失败!\n好友：{del_qq}不在好友推送列表', event=event)
        else:
            qq_friend_list.remove(del_qq)
            obj['qq_friend_list'] = qq_friend_list
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
            await nonebot.get_bot().send(user_id=user_id, message=f'已将好友：{del_qq}移出推送列表！', event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'出错了!\n错误日志:{e}', at_sender=True, event=event)


# 机器人主人使用，用于添加推送群聊
add_group_list = on_command('添加推送群聊', permission=SUPERUSER)


@add_group_list.handle()
async def add_group_list(event: Event):
    try:
        # 读取需要推送的群
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_group_list = obj['qq_group_list']
        user_id = int(str(event.get_user_id()))
        add_group = int(str(event.get_message()).split('#')[-1])
        if add_group not in qq_group_list:
            await nonebot.get_bot().send(user_id=user_id, message=f'已将群：{add_group}加入推送列表', event=event)
            qq_group_list.append(add_group)
            obj['qq_group_list'] = qq_group_list
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
        else:
            await nonebot.get_bot().send(user_id=user_id, message=f'加入失败！\n群：{add_group}已经在推送列表中了', event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'出错了!\n错误日志:{e}', at_sender=True, event=event)


# 机器人主人使用，用于删除推送群聊
del_group_list = on_command('删除推送群聊', permission=SUPERUSER)


@del_group_list.handle()
async def del_group_list(event: Event):
    try:
        # 读取需要推送的群
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_group_list = obj['qq_group_list']
        user_id = int(str(event.get_user_id()))
        del_group = int(str(event.get_message()).split('#')[-1])
        if del_group not in qq_group_list:
            await nonebot.get_bot().send(user_id=user_id, message=f'删除失败！\n群：{del_group}不在推送列表', event=event)
        else:
            qq_group_list.remove(del_group)
            obj['qq_group_list'] = qq_group_list
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
            await nonebot.get_bot().send(user_id=user_id, message=f'已将群：{del_group}移出推送列表！', event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'出错了!\n错误日志:{e}', at_sender=True, event=event)


# 机器人主人使用，用于查询推送群聊列表
index_group_list = on_command('查询推送群聊列表', permission=SUPERUSER)


@index_group_list.handle()
async def index_group_list(event: Event):
    try:
        # 读取需要推送的群
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_group_list = obj['qq_group_list']
        user_id = int(str(event.get_user_id()))
        if qq_group_list:
            group = ''
            for i in qq_group_list:
                group = group + '群：' + str(i) + '\n' + ''
            await nonebot.get_bot().send(user_id=user_id, message=group, at_sender=True, event=event)
        else:
            await nonebot.get_bot().send(user_id=user_id, message='暂无推送群聊！', event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'查询失败！\n错误日志：{e}', event=event)


# 机器人主人使用，用于查询推送好友列表
index_qq_list = on_command('查询推送好友列表', permission=SUPERUSER)


@index_qq_list.handle()
async def index_qq_list(event: Event):
    try:
        # 读取需要推送的好友
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_friend_list = obj['qq_friend_list']
        user_id = int(str(event.get_user_id()))
        if qq_friend_list:
            group = ''
            for i in qq_friend_list:
                group = group + '好友：' + str(i) + '\n' + ''
            await nonebot.get_bot().send(user_id=user_id, message=group, at_sender=True, event=event)
        else:
            await nonebot.get_bot().send(user_id=user_id, message='暂无推送好友！', event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f'查询失败！\n错误日志：{e}', event=event)


# 机器人主人使用，同意好友添加机器人请求
agree_qq_add = on_command('同意添加好友', permission=SUPERUSER)


@agree_qq_add.handle()
async def agree_qq_add(event: Event):
    try:
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq = obj['add_qq_req_list']['qq']
        flag = obj['add_qq_req_list']['flag']
        user_id = int(event.get_user_id())
        agree_id = int(str(event.get_message()).split('#')[-1])
        if agree_id in qq:
            await nonebot.get_bot().send(user_id=user_id, message=f'机器人成功添加QQ:{agree_id}为好友！', event=event)
            await nonebot.get_bot().set_friend_add_request(flag=flag, approve=True, remark='')
            qq.remove(agree_id)
            flag = ''
            obj['add_qq_req_list']['qq'] = qq
            obj['add_qq_req_list']['flag'] = flag
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)

        else:
            await nonebot.get_bot().send(user_id=user_id, message=f'QQ:{agree_id}不在好友申请列表！', event=event)
    except Exception as e:
        for su_qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(su_qq), message=f'机器人出错了\n错误信息：{e}')


# 以下为基础指令，所有好友皆可用
# 获取大学习答案
college_study = on_command('青年大学习', aliases={'大学习'}, priority=5)


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


# 获取大学习完成截图
complete_Scr = on_command('大学习截图', aliases={'完成截图'}, priority=5)


@complete_Scr.handle()
async def complete_Scr(bot: Bot, event: Event, state: T_State):
    try:
        content = await get_pic()
        scr = content[3]
        if scr is None:
            await nonebot.get_bot().send(message="本周暂未更新青年大学习", at_sender=True, event=event)
        else:
            await nonebot.get_bot().send(message=MessageSegment.image(scr), at_sender=True, event=event)
    except Exception as e:
        await nonebot.get_bot().send(message=f"出错了，错误信息：{e}", at_sender=True, event=event)
        logger.error(f"{datetime.now()}: 错误信息：{e}")


# 开启大学习定时更新推送
recover_task = on_command('开启大学习推送', priority=5)


@recover_task.handle()
async def recover_task(event: Event):
    try:
        # 读取需要推送的好友
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_friend_list = obj['qq_friend_list']
        user_id = int(str(event.get_user_id()))
        if user_id not in qq_friend_list:
            await nonebot.get_bot().send(user_id=user_id, message='青年大学习定时更新推送开启成功!', event=event)
            qq_friend_list.append(user_id)
            obj['qq_friend_list'] = qq_friend_list
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
        else:
            await nonebot.get_bot().send(user_id=user_id, message='你已经开启了青年大学习定时更新推送了！', event=event)
    except:
        await nonebot.get_bot().send(message='出错了!请询问机器人主人以解决问题！', event=event)


# 关闭大学习定时更新推送
close_task = on_command('关闭大学习推送', priority=5)


@close_task.handle()
async def close_task(event: Event):
    try:
        # 读取需要推送的好友
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq_friend_list = obj['qq_friend_list']
        user_id = int(str(event.get_user_id()))
        if user_id not in qq_friend_list:
            await nonebot.get_bot().send(user_id=user_id, message='你已经关闭青年大学习定时更新推送了！!', event=event)
        else:
            qq_friend_list.remove(user_id)
            obj['qq_friend_list'] = qq_friend_list
            with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
                json.dump(obj, f1, indent=4)
            await nonebot.get_bot().send(user_id=user_id, message='青年大学习定时更新推送关闭成功!', event=event)
    except:
        await nonebot.get_bot().send(message='出错了!请询问机器人主人以解决问题！', event=event)


# 大学习帮助功能
help_list = on_command('功能', aliases={'菜单', '帮助', 'help'}, priority=5)


@help_list.handle()
async def help_list(event: Event):
    try:
        _help = '大学习功能指令\n主人专用:\n1、添加(删除)推送群聊#群号\n2、添加(删除)推送好友#QQ号\n3、查询推送好友(群聊)列表\n4、全局开启(关闭)大学习推送或全局开启(关闭)推送\n5、同意添加好友#QQ号\n' + \
                '全员可用功能:\n1、开启(关闭)大学习推送\n2、青年大学习或大学习\n3、大学习截图或完成截图\n4、帮助、菜单、功能和help '
        await nonebot.get_bot().send(message=_help, at_sender=True, event=event)
    except:
        await nonebot.get_bot().send(message='出错了!请询问机器人主人以解决问题！', event=event)


# 机器人推送添加机器人好友请求事件
add_friend = on_request(priority=1, block=True)


@add_friend.handle()
async def add_friend(event: FriendRequestEvent):
    try:
        with open(pathlib.Path(__file__).with_name('set.json'), 'r', encoding='utf-8') as f:
            obj = json.load(f)
        qq = obj['add_qq_req_list']['qq']
        add_req = json.loads(event.json())
        add_qq = add_req['user_id']
        qq.append(add_qq)
        comment = add_req['comment']
        flag = add_req['flag']
        realtime = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(add_req['time']))
        obj['add_qq_req_list']['qq'] = qq
        obj['add_qq_req_list']['flag'] = flag
        with open(pathlib.Path(__file__).with_name('set.json'), 'w', encoding='utf-8') as f1:
            json.dump(obj, f1, indent=4)
        for su_qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(su_qq),
                                             message=f'QQ：{add_qq}请求添加机器人为好友!\n请求添加时间：{realtime}\n验证信息为：{comment}')
    except Exception as e:
        for su_qq in super_id:
            await nonebot.get_bot().send_msg(user_id=int(su_qq), message=f'机器人出错了\n错误信息：{e}')
