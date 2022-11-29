# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}arti <word>`
    Dapatkan arti kata tersebut.

• `{i}sinonim <word>`
    Dapatkan semua sinonim.

• `{i}antonim <word>`
    Dapatkan semua antonim.

• `{i}ud <word>`
    Ambil definisi kata dari kamus perkotaan.
"""
import io

from Ayra.fns.misc import get_synonyms_or_antonyms
from Ayra.fns.tools import async_searcher

from . import get_string, ayra_cmd


@ayra_cmd(pattern="arti( (.*)|$)", manager=True)
async def mean(event):
    wrd = event.pattern_match.group(1).strip()
    if not wrd:
        return await event.eor(get_string("wrd_4"))
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{wrd}"
    out = await async_searcher(url, re_json=True)
    try:
        return await event.eor(f'**{out["title"]}**')
    except (KeyError, TypeError):
        pass
    defi = out[0]["meanings"][0]["definitions"][0]
    ex = defi["example"] if defi.get("example") else "None"
    text = get_string("wrd_1").format(wrd, defi["definition"], ex)
    if defi.get("synonyms"):
        text += (
            f"\n\n• **{get_string('wrd_5')} :**"
            + "".join(f" {a}," for a in defi["synonyms"])[:-1][:10]
        )
    if defi.get("antonyms"):
        text += (
            f"\n\n**{get_string('wrd_6')} :**"
            + "".join(f" {a}," for a in defi["antonyms"])[:-1][:10]
        )
    if len(text) > 4096:
        with io.BytesIO(str.encode(text)) as fle:
            fle.name = f"{wrd}-meanings.txt"
            await event.reply(
                file=fle,
                force_document=True,
                caption=f"Arti dari {wrd}",
            )
            await event.delete()
    else:
        await event.eor(text)


@ayra_cmd(
    pattern="(sinonim|antonim)",
)
async def mean(event):
    task = event.pattern_match.group(1) + "nyms"
    try:
        wrd = event.text.split(maxsplit=1)[1]
    except IndexError:
        return await event.eor("Berikan Sesuatu untuk dicari..")
    try:
        ok = await get_synonyms_or_antonyms(wrd, task)
        x = get_string("wrd_2" if task == "synonyms" else "wrd_3").format(wrd)
        for c, i in enumerate(ok, start=1):
            x += f"**{c}.** `{i}`\n"
        if len(x) > 4096:
            with io.BytesIO(str.encode(x)) as fle:
                fle.name = f"{wrd}-{task}.txt"
                await event.client.send_file(
                    event.chat_id,
                    fle,
                    force_document=True,
                    allow_cache=False,
                    caption=f"{task} of {wrd}",
                    reply_to=event.reply_to_msg_id,
                )
                await event.delete()
        else:
            await event.eor(x)
    except Exception as e:
        await event.eor(
            get_string("wrd_7" if task == "synonyms" else "wrd_8").format(e)
        )


@ayra_cmd(pattern="ud (.*)")
async def _(event):
    word = event.pattern_match.group(1).strip()
    if not word:
        return await event.eor(get_string("autopic_1"))
    out = await async_searcher(
        "http://api.urbandictionary.com/v0/define", params={"term": word}, re_json=True
    )
    try:
        out = out["list"][0]
    except IndexError:
        return await event.eor(get_string("autopic_2").format(word))
    await event.eor(
        get_string("wrd_1").format(out["word"], out["definition"], out["example"]),
    )
