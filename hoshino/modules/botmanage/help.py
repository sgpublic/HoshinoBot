from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
====================
= HoshinoBot使用说明 =
====================
发送[]内的关键词触发

==== 查看详细说明 ====
[帮助pcr查询]
[帮助pcr娱乐][帮助pcr订阅]
[帮助通用]

====== 常用指令 ======
[怎么拆日和] 竞技场查询
[pcr速查] 常用网址
[星乃来发十连] 转蛋模拟

[切噜一下+待加密文本]
▲切噜语转换
[来杯咖啡+反馈内容]
▲联系维护组

====== 模块开关 ======
※限群管理/群主控制※
[lssv] 查看各模块开关状态
[启用+空格+service]
[禁用+空格+service]
 
=====================
※Hoshino开源Project：
github.com/Ice9Coffee/HoshinoBot
您对项目作者的支持与Star是本bot更新维护的动力
💰+⭐=❤
'''.strip()
# 魔改请保留 github.com/Ice9Coffee/HoshinoBot 项目地址


def gen_service_manual(service: Service, gid: int):
    spit_line = '=' * max(0, 18 - len(service.name))
    manual = [f"|{'○' if service.check_enabled(gid) else '×'}| {service.name} {spit_line}"]
    if service.help:
        manual.append(service.help)
    return '\n'.join(manual)


def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for s in service_list:
        if s.visible:
            manual.append(gen_service_manual(s, gid))
    return '\n'.join(manual)


@sv.on_suffix('help', '帮助')
async def send_help(bot, ev: CQEvent):
    gid = ev.group_id
    arg = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    services = Service.get_loaded_services()
    if not arg:
        await bot.send(ev, TOP_MANUAL)
    elif arg in bundles:
        msg = gen_bundle_manual(arg, bundles[arg], gid)
        await bot.send(ev, msg)
    elif arg in services:
        s = services[arg]
        msg = gen_service_manual(s, gid)
        await bot.send(ev, msg)
    # else: ignore
