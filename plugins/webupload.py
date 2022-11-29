# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}webupload`
    Unggah file di server lain.
"""

import os

from Ayra.fns.tools import _webupload_cache

from . import Button, asst, get_string, ayra_cmd


@ayra_cmd(
    pattern="webupload( (.*)|$)",
)
async def _(event):
    xx = await event.eor(get_string("com_1"))
    match = event.pattern_match.group(1).strip()
    if event.chat_id not in _webupload_cache:
        _webupload_cache.update({int(event.chat_id): {}})
    if match:
        if not os.path.exists(match):
            return await xx.eor("`Berkas tidak ada.`")
        _webupload_cache[event.chat_id][event.id] = match
    elif event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if reply.photo:
            file = await reply.download_media("resources/downloads/")
            _webupload_cache[int(event.chat_id)][int(event.id)] = file
        else:
            file, _ = await event.client.fast_downloader(
                reply.document, show_progress=True, event=xx
            )
            _webupload_cache[int(event.chat_id)][int(event.id)] = file.name
    else:
        return await xx.eor("`Balas ke file atau berikan jalur file...`")
    if not event.client._bot:
        results = await event.client.inline_query(
            asst.me.username, f"fl2lnk {event.chat_id}:{event.id}"
        )
        await results[0].click(event.chat_id, reply_to=event.reply_to_msg_id)
        await xx.delete()

    else:
        __cache = f"{event.chat_id}:{event.id}"
        buttons = [
            [
                Button.inline("anonfiles", data=f"flanonfiles//{__cache}"),
                Button.inline("transfer", data=f"fltransfer//{__cache}"),
            ],
            [
                Button.inline("bayfiles", data=f"flbayfiles//{__cache}"),
                Button.inline("x0.at", data=f"flx0.at//{__cache}"),
            ],
            [
                Button.inline("file.io", data=f"flfile.io//{__cache}"),
                Button.inline("siasky", data=f"flsiasky//{__cache}"),
            ],
        ]
        await xx.edit("**Choose Server to Upload File...**", buttons=buttons)
