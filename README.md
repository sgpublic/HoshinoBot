# HoshinoBot

[![License](https://img.shields.io/github/license/Ice9Coffee/HoshinoBot)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![Nonebot Version](https://img.shields.io/badge/nonebot-1.6.0%2B%2C%202.0.0---blue)

这里是 HoshinoBot 的第三方维护版本。

## 原 HoshinoBot 官方社区及赞助方式

[![试用/赞助群](https://img.shields.io/badge/试用/赞助-Hoshinoのお茶会-brightgreen)](https://jq.qq.com/?_wv=1027&k=eYGgrL4A)
[![开发交流群](https://img.shields.io/badge/开发交流-Hoshinoの4番灵装-brightgreen)](https://jq.qq.com/?_wv=1027&k=6zyqKSqT)
[![防炸群备胎](https://img.shields.io/badge/开发交流-Hoshinoの5番灵装-brightgreen)](https://jq.qq.com/?_wv=1027&k=WYcls71E)
[![Telegram](https://img.shields.io/badge/Telegram-后花园国际部-blue)](https://t.me/+u2Sv4sS-8CEwZjc1)

## 简介

**HoshinoBot:** 基于 [nonebot](https://docs.nonebot.dev/) 的开源Q群bot框架。

## 功能介绍

HoshinoBot 的功能开发以服务 [公主连结☆Re:Dive](http://priconne-redive.jp) 玩家为核心。

<details>
  <summary>主要功能</summary>

- **竞技场解法查询**：支持按服务器过滤，支持反馈点赞点踩
- **竞技场结算提醒**
- **公会战管理**
- **Rank推荐表搬运**
- **官方推特转发**
- **官方四格推送**
- **角色别称转换**
- **切噜语编解码**：切噜～♪
- **竞技场余矿查询**

</details>

-------------

### 功能模块控制

HoshinoBot 的功能繁多，各群可根据自己的需要进行开关控制，群管理发送 `lssv` 即可查看功能模块的启用状态，使用以下命令进行控制：

```
启用 service-name
禁用 service-name
```

## 开源协议及免责声明

本项目遵守GPL-3.0协议开源，请在协议允许的条件及范围内使用本项目。本项目的开发者不会强制向您索要任何费用，同时也不会提供任何质保，一切因本项目引起的法律、利益纠纷由与本项目的开发者无关。
- 对于自行搭建、小范围私用的非营利性bot，若遇到任何部署、开发上的疑问，欢迎提交issue或加入[开发交流群](https://jq.qq.com/?_wv=1027&k=6zyqKSqT)（如炸群请加备用群[星乃の5番灵装](https://jq.qq.com/?_wv=1027&k=WYcls71E)）讨论，我们欢迎有礼貌、描述详尽的提问！
- 对于以营利为目的部署的bot，由部署者负责，与本项目的开发者无关，本项目的开发者及社区没有义务回答您部署时的任何疑问。
- 对于HoshinoBot插件的开发者，在您发布插件或利用插件营利时，请遵守GPL-3.0协议将插件代码开源。

最终解释权归HoshinoBot开发组所有。


## 部署指南

本仓库维护的版本仅支持在 Linux 上开箱即用，不建议在 Windows 上使用。

### 直接运行

将项目克隆到你喜欢的目录并进入，例如 `~/nonebot-hoshino`，随后直接运行 `start` 脚本即可。

### Docker

在你喜欢的位置创建一个目录并进入，例如 `~/nonebot-hoshino`，随后将项目克隆到当前目录的 `app` 目录下：

```shell
git clone https://github.com/sgpublic/HoshinoBot --depth=1 ./app
```

然后将 `docker-compose.yaml` 文件写入当前目录，`docker-compose.yaml` 示例：

```yaml
version: '3'
services:
  hoshino:
    image: mhmzx/poetry-runner:bullseye-20240311
    container_name: nonebot-hoshino
    volumes:
      - ./app:/app
      - ./config:/app/hoshino/config
      - ./cache:/home/poetry-runner/.cache
      - ./res/cache:/app/res/cache
    network_mode: host
    restart: unless-stopped
```

其中 `mhmzx/poetry-runner` 为专为 nonebot 机器人的 python 项目制作的镜像，包含各种常用依赖以及开箱即用的启动脚本，详见 [sgpublic/poetry-docker](https://github.com/sgpublic/poetry-docker)。

最后启动即可：

```shell
docker-compose up -d
```


## 友情链接

**干炸里脊资源站**: https://redive.estertion.win/

**公主连结Re: Dive Fan Club - 硬核的竞技场数据分析站**: https://pcrdfans.com/

**yobot**: https://yobot.win/

