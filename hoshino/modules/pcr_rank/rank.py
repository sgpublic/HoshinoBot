import os

from aiocqhttp import MessageSegment

from hoshino.R import ResObj, ResImg, get
from . import sv
from hoshino.priv import *
from hoshino import aiorequests
from os import path
import json
from nonebot import scheduler
from hoshino.config.__bot__ import PCR_RANK

config = PCR_RANK
server_addr = config['upstream']
resize_pic = config['resize_pic']


def cache_obj(path, *paths):
    return ResObj(os.path.join('cache', 'pcr-rank', path, *paths))


def cache_img(path, *paths):
    return ResImg(os.path.join('cache', 'pcr-rank', 'pic', path, *paths))


async def load_config():
    if not (cache := get('cache', 'pcr-rank')).exist:
        os.mkdir(cache.path)
    if not (pic := get('cache', 'pcr-rank', 'pic')).exist:
        os.mkdir(pic.path)
    await update_cache()


def save_config():
    config_path = path.join(path.dirname(__file__), "config.json")
    with open(config_path, 'r+', encoding='utf8') as fp:
        fp.seek(0)
        fp.truncate()
        str = json.dumps(config, indent=4, ensure_ascii=False)
        fp.write(str)


async def download_rank_pic(url):
    sv.logger.info(f"正在下载{url}")
    resp = await aiorequests.head(url)
    content_length = int(resp.headers["Content-Length"])
    sv.logger.info(f"块大小{str(content_length)}")
    # 分割200kb下载
    block_size = 1024 * 200
    range_list = []
    current_start_bytes = 0
    while True:
        if current_start_bytes + block_size >= content_length:
            range_list.append(f"{str(current_start_bytes)}-{str(content_length)}")
            break
        range_list.append(f"{str(current_start_bytes)}-{str(current_start_bytes + block_size)}")
        current_start_bytes += block_size + 1
    pic_bytes_list = []
    for block in range_list:
        sv.logger.info(f"正在下载块{block}")
        headers = {"Range": f"bytes={block}"}
        resp = await aiorequests.get(url, headers=headers)
        res_content = await resp.content
        pic_bytes_list.append(res_content)
    return b"".join(pic_bytes_list)


async def update_rank_pic_cache(force_update: bool):
    config_names = ["cn", "tw", "jp"]
    for conf_name in config_names:
        config_path = cache_obj(f"{conf_name}.json").path
        with open(config_path, "r", encoding="utf8") as fp:
            rank_config = json.load(fp)
        for img_name in rank_config["files"]:
            if not force_update:
                if cache_img(f"{conf_name}_{img_name}").exist:
                    continue
            rank_img_url = f"{server_addr}{config['source'][conf_name]['channel']}/{config['source'][conf_name]['route']}/{img_name}"
            img_content = await download_rank_pic(rank_img_url)
            with open(cache_img(f"{conf_name}_{img_name}").path, 'ab') as fp:
                fp.seek(0)
                fp.truncate()
                fp.write(img_content)


async def update_cache(force_update: bool = False):
    sv.logger.info("正在更新Rank表缓存")
    config_names = ["cn", "tw", "jp"]
    for conf_name in config_names:
        resp = await aiorequests.get(
            f"{server_addr}{config['source'][conf_name]['channel']}/{config['source'][conf_name]['route']}/config.json")
        res = await resp.text
        with open(cache_obj(f"{conf_name}.json").path, "a", encoding="utf8") as fp:
            fp.seek(0)
            fp.truncate()
            fp.write(res)
    await update_rank_pic_cache(force_update)
    sv.logger.info("Rank表缓存更新完毕")


@sv.on_rex(r"^(\*?([日台国陆b])服?([前中后]*)卫?)?rank(表|推荐|指南)?$")
async def rank_sheet(bot, ev):
    if config == None:
        await load_config()
    match = ev["match"]
    is_jp = match.group(2) == "日"
    is_tw = match.group(2) == "台"
    is_cn = match.group(2) and match.group(2) in "国陆b"
    if not is_jp and not is_tw and not is_cn:
        await bot.send(ev, "\n请问您要查询哪个服务器的rank表？\n*日rank表\n*台rank表\n*陆rank表", at_sender=True)
        return
    msg = [
        MessageSegment.text("\n")
    ]
    if is_jp:
        rank_config_path = cache_obj("jp.json").path
        with open(rank_config_path, "r", encoding="utf8") as fp:
            rank_config = json.load(fp)
        rank_imgs = []
        for img_name in rank_config["files"]:
            rank_imgs.append(cache_img(f"jp_{img_name}").cqcode)
        msg.append(MessageSegment.text(rank_config["notice"]))
        pos = match.group(3)
        if not pos or "前" in pos:
            msg.append(rank_imgs[0])
        if not pos or "中" in pos:
            msg.append(rank_imgs[1])
        if not pos or "后" in pos:
            msg.append(rank_imgs[2])
        await bot.send(ev, msg, at_sender=True)
    elif is_tw:
        rank_config_path = cache_obj("tw.json").path
        with open(rank_config_path, "r", encoding="utf8") as fp:
            rank_config = json.load(fp)
        rank_imgs = []
        for img_name in rank_config["files"]:
            rank_imgs.append(cache_img(f"tw_{img_name}").cqcode)
        msg.append(MessageSegment.text(rank_config["notice"]))
        for rank_img in rank_imgs:
            msg.append(rank_img)
        await bot.send(ev, "".join(msg), at_sender=True)
    elif is_cn:
        rank_config_path = cache_obj("cn.json").path
        with open(rank_config_path, "r", encoding="utf8") as fp:
            rank_config = json.load(fp)
        rank_imgs = []
        for img_name in rank_config["files"]:
            rank_imgs.append(cache_img(f"cn_{img_name}").cqcode)
        msg.append(MessageSegment.text(rank_config["notice"]))
        for rank_img in rank_imgs:
            msg.append(rank_img)
        await bot.send(ev, msg, at_sender=True)


@sv.on_fullmatch("查看当前rank更新源")
async def show_current_rank_source(bot, ev):
    await load_config()
    if not check_priv(ev, SUPERUSER):
        await bot.send(ev, "仅有SUPERUSER可以使用本功能")
    msg = []
    msg.append("\n")
    msg.append("国服:\n")
    msg.append(config["source"]["cn"]["name"])
    msg.append("   ")
    if config["source"]["cn"]["channel"] == "stable":
        msg.append("稳定源")
    elif config["source"]["cn"]["channel"] == "auto_update":
        msg.append("自动更新源")
    else:
        msg.append(config["source"]["cn"]["channel"])
    msg.append("\n台服:\n")
    msg.append(config["source"]["tw"]["name"])
    msg.append("   ")
    if config["source"]["tw"]["channel"] == "stable":
        msg.append("稳定源")
    elif config["source"]["tw"]["channel"] == "auto_update":
        msg.append("自动更新源")
    else:
        msg.append(config["source"]["tw"]["channel"])
    msg.append("\n日服:\n")
    msg.append(config["source"]["jp"]["name"])
    msg.append("   ")
    if config["source"]["jp"]["channel"] == "stable":
        msg.append("稳定源")
    elif config["source"]["jp"]["channel"] == "auto_update":
        msg.append("自动更新源")
    else:
        msg.append(config["source"]["jp"]["channel"])
    await bot.send(ev, "".join(msg), at_sender=True)


@sv.on_fullmatch("查看全部rank更新源")
async def show_all_rank_source(bot, ev):
    await load_config()
    if not check_priv(ev, SUPERUSER):
        await bot.send(ev, "仅有SUPERUSER可以使用本功能")
    resp = await aiorequests.get(server_addr + "route.json")
    res = await resp.json()
    msg = []
    msg.append("\n")
    msg.append("稳定源：\n国服:\n")
    for uo in res["ranks"]["channels"]["stable"]["cn"]:
        msg.append(uo["name"])
        msg.append("   ")
    msg.append("\n台服:\n")
    for uo in res["ranks"]["channels"]["stable"]["tw"]:
        msg.append(uo["name"])
        msg.append("   ")
    msg.append("\n日服:\n")
    for uo in res["ranks"]["channels"]["stable"]["jp"]:
        msg.append(uo["name"])
        msg.append("   ")
    msg.append("\n自动更新源：\n国服:\n")
    for uo in res["ranks"]["channels"]["auto_update"]["cn"]:
        msg.append(uo["name"])
        msg.append("   ")
    msg.append("\n台服:\n")
    for uo in res["ranks"]["channels"]["auto_update"]["tw"]:
        msg.append(uo["name"])
        msg.append("   ")
    msg.append("\n日服:\n")
    for uo in res["ranks"]["channels"]["auto_update"]["jp"]:
        msg.append(uo["name"])
        msg.append("   ")
    msg.append("\n如需修改更新源，请使用命令[设置rank更新源 国/台/日 稳定/自动更新 源名称]")
    await bot.send(ev, "".join(msg), at_sender=True)


@sv.on_fullmatch("更新rank表缓存")
async def update_rank_cache(bot, ev):
    await load_config()
    if not check_priv(ev, SUPERUSER):
        await bot.send(ev, "仅有SUPERUSER可以使用本功能")
    await update_cache()
    await bot.send(ev, "更新成功")


@scheduler.scheduled_job('cron', hour='17', minute='06')
async def schedule_update_rank_cache():
    await load_config()
    await update_cache()
