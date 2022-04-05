<div align="center">
    <img src="https://s4.ax1x.com/2022/03/05/bw2k9A.png" alt="bw2k9A.png" border="0"/>
    <h1>nonebot_plugin_youthstudy</h1>
    <b>基于nonebot2的青年大学习插件，用于获取最新一期青年大学习答案</b>
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



### 正式使用

对机器人发送口令：“青年大学习”或者“大学习”即可获取最新一期的青年大学习答案



### TODO

- [ ] 通过检查更新自动提醒完成青年大学习



## 更新日志

### 2021/3/5

- 支持nonebot[v2.0.0-beta2]，请更新至最新版nonebot使用

