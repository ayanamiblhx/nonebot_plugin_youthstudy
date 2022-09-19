<div align="center">
    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>
    <h1>nonebot_plugin_youthstudy</h1>
    <b>✨基于nonebot2的青年大学习插件，用于获取最新一期青年大学习答案✨</b>
    <br/>
    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>
    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>
    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>
    <a href="https://github.com/ayanamiblhx/nonebot_plugin_youthstudy/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ayanamiblhx/nonebot_plugin_youthstudy?style=flat-square"></a>
</div>


## 安装及更新

- 使用`nb plugin install nonebot_plugin_youthstudy`或者`pip install nonebot_plugin_youthstudy`来进行安装
- 使用`nb plugin update nonebot_plugin_youthstudy`或者`pip install nonebot_plugin_youthstudy -U`来进行更新

### 导入插件(两种方式二选一)

- 在`bot.py`中添加`nonebot.load_plugin("nonebot_plugin_youthstudy")`

- 在`pyproject.toml`里的`[tool.nonebot]`中添加`plugins = ["nonebot_plugin_youthstudy"]`

**注**：如果你使用`nb`安装插件，则不需要设置此项

### 添加配置

- 运行一遍bot，然后关闭

- 在bot目录的data目录下修改`study_config.json`文件，添加如下配置：

    - `"SUPER_USERS": ["超级用户qq号"]`

### 正式使用

| 命令                    | 举例               | 说明                                                         |
| ----------------------- | ------------------ | ------------------------------------------------------------ |
| 青年大学习/大学习       | 青年大学习         | 获取大学习答案                                               |
| 开启/关闭大学习推送     | 开启大学习推送     | 在群聊中仅有超级用户能开启推送，私聊任何人都能开启推送，但需要加好友 |
| 开启/关闭大学习全局推送 | 关闭大学习全局推送 | 关闭全局推送后，所有的群聊、私聊推送任务都会关闭，仅超级用户使用 |
| 同意/拒绝+qq号          | 同意1234567        | 处理好友请求，仅超级用户使用                                 |
| 同意/拒绝所有好友请求   | 拒绝所有好友请求   | 拒绝所有的好友请求，仅超级用户使用                           |
| 大学习截图              | 大学习截图         | 获取主页截图                                                 |
| 完成截图                | 完成截图           | 获取大学习完成截图                                           |
| 大学习帮助              | 大学习帮助         | 获取命令列表                                                 |

### TODO

- [ ] 优化机器人

## 更新日志

### 2022/9/19

- 增加异常抓取

### 2022/9/12

- 修复获取答案失败的bug

### 2022/9/8

- 修复无法获取截图的bug

### 2022/6/17

- 修复bug，降低python版本要求为>=3.8

### 2022/5/7

- 代码重构

### 2022/4/24

- 支持对机器人发送口令开关定时推送功能
- 支持对机器人发指令设置推送相关好友/群聊

### 2022/4/18

- 支持自动获取青年大学习完成截图功能。如果您所在学校会查后台观看记录，请前往相应平台观看1分钟，确保留下观看记录！

### 2022/4/17

- 支持通过检查更新自动提醒完成青年大学习，请参照机器人配置进行配置

### 2022/3/5

- 支持nonebot[v2.0.0-beta2]，请更新至最新版nonebot使用

