# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}eod`
    `Dapatkan Acara Hari Ini`

• `{i}pntrst <link/id>`
    Unduh dan kirim pinterest

• `{i}gadget <search query>`
    Pencarian Gadget dari Telegram.

• `{i}randomuser`
   Hasilkan detail tentang pengguna acak.

• `{i}ascii <reply image>`
    Ubah gambar balasan menjadi html.
"""

import os
from datetime import datetime as dt

from bs4 import BeautifulSoup as bs

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None
try:
    from img2html.converter import Img2HTMLConverter
except ImportError:
    Img2HTMLConverter = None

from . import async_searcher, get_random_user_data, get_string, re, ayra_cmd


@ayra_cmd(pattern="eod$")
async def diela(e):
    m = await e.eor(get_string("com_1"))
    li = "https://daysoftheyear.com"
    te = "🎊 **Events of the Day**\n\n"
    da = dt.now()
    month = da.strftime("%b")
    li += f"/days/{month}/" + da.strftime("%F").split("-")[2]
    ct = await async_searcher(li, re_content=True)
    bt = bs(ct, "html.parser", from_encoding="utf-8")
    ml = bt.find_all("a", "js-link-target", href=re.compile("daysoftheyear.com/days"))
    for eve in ml[:5]:
        te += f'• [{eve.text}]({eve["href"]})\n'
    await m.edit(te, link_preview=False)


@ayra_cmd(
    pattern="pntrst( (.*)|$)",
)
async def pinterest(e):
    m = e.pattern_match.group(1).strip()
    if not m:
        return await e.eor("`Berikan tautan pinterest.`", time=3)
    soup = await async_searcher(
        "https://www.expertstool.com/download-pinterest-video/",
        data={"url": m},
        post=True,
    )
    try:
        _soup = bs(soup, "html.parser").find("table").tbody.find_all("tr")
    except BaseException:
        return await e.eor("`Tautan salah atau pin pribadi.`", time=5)
    file = _soup[1] if len(_soup) > 1 else _soup[0]
    file = file.td.a["href"]
    await e.client.send_file(e.chat_id, file, caption=f"Pin:- {m}")


@ayra_cmd(pattern="gadget( (.*)|$)")
async def mobs(e):
    mat = e.pattern_match.group(1).strip()
    if not mat:
        await e.eor("Harap Beri Nama Ponsel untuk dicari.")
    query = mat.replace(" ", "%20")
    jwala = f"https://gadgets.ndtv.com/search?searchtext={query}"
    c = await async_searcher(jwala)
    b = bs(c, "html.parser", from_encoding="utf-8")
    co = b.find_all("div", "rvw-imgbox")
    if not co:
        return await e.eor("Tidak ada hasil yang ditemukan!")
    bt = await e.eor(get_string("com_1"))
    out = "**📱 Mobile / Gadgets Search**\n\n"
    li = co[0].find("a")
    imu, title = None, li.find("img")["title"]
    cont = await async_searcher(li["href"])
    nu = bs(cont, "html.parser", from_encoding="utf-8")
    req = nu.find_all("div", "_pdsd")
    imu = nu.find_all(
        "img", src=re.compile("https://i.gadgets360cdn.com/products/large/")
    )
    if imu:
        imu = imu[0]["src"].split("?")[0] + "?downsize=*:420&output-quality=80"
    out += f"☑️ **[{title}]({li['href']})**\n\n"
    for fp in req:
        ty = fp.findNext()
        out += f"- **{ty.text}** - `{ty.findNext().text}`\n"
    out += "_"
    if imu == []:
        imu = None
    await e.reply(out, file=imu, link_preview=False)
    await bt.delete()


@ayra_cmd(pattern="randomuser")
async def _gen_data(event):
    x = await event.eor(get_string("com_1"))
    msg, pic = await get_random_user_data()
    await event.reply(file=pic, message=msg)
    await x.delete()


@ayra_cmd(
    pattern="ascii( (.*)|$)",
)
async def _(e):
    if not Img2HTMLConverter:
        return await e.eor("'img2html-converter' not installed!")
    if not e.reply_to_msg_id:
        return await e.eor(get_string("ascii_1"))
    m = await e.eor(get_string("ascii_2"))
    img = await (await e.get_reply_message()).download_media()
    char = e.pattern_match.group(1).strip() or "■"
    converter = Img2HTMLConverter(char=char)
    html = converter.convert(img)
    shot = WebShot(quality=85)
    pic = await shot.create_pic_async(html=html)
    await m.delete()
    await e.reply(file=pic)
    os.remove(pic)
    os.remove(img)
