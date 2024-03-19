import itertools
import os.path
from datetime import datetime

from io import BytesIO
from PIL import Image

from hoshino import util, R, log, aiorequests
from hoshino.config import DEBUG, SUPERUSERS
from hoshino.typing import CQEvent
from . import sv


@sv.on_fullmatch('千里眼')
async def future_gacha(bot, ev):
    await bot.send(ev, "亿里眼·一之章 nga.178.com/read.php?tid=21317816\n亿里眼·二之章 nga.178.com/read.php?tid=25358671")
    await util.silence(ev, 60)
