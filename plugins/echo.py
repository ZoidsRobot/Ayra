# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from . import get_help

__doc__ = get_help("help_echo")


from telethon.utils import get_display_name

from Ayra.dB.echo_db import add_echo, check_echo, list_echo, rem_echo

from . import LOGS, events, ayra_bot, ayra_cmd


@ayra_cmd(pattern="addecho( (.*)|$)")
async def echo(e):
    r = await e.get_reply_message()
    if r:
        user = r.sender_id
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await e.client.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await e.eor("Reply To A user.", time=5)
    if check_echo(e.chat_id, user):
        return await e.eor("Echo already activated for this user.", time=5)
    add_echo(e.chat_id, user)
    ok = await e.client.get_entity(user)
    user = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
    await e.eor(f"Activated Echo For {user}.")


@ayra_cmd(pattern="remecho( (.*)|$)")
async def rm(e):
    r = await e.get_reply_message()
    if r:
        user = r.sender_id
    else:
        try:
            user = e.text.split()[1]
            if user.startswith("@"):
                ok = await e.client.get_entity(user)
                user = ok.id
            else:
                user = int(user)
        except BaseException:
            return await e.eor("Reply To A User.", time=5)
    if check_echo(e.chat_id, user):
        rem_echo(e.chat_id, user)
        ok = await e.client.get_entity(user)
        user = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
        return await e.eor(f"Deactivated Echo For {user}.")
    await e.eor("Echo not activated for this user")


@ayra_bot.on(events.NewMessage(incoming=True))
async def okk(e):
    if check_echo(e.chat_id, e.sender_id):
        try:
            ok = await e.client.get_messages(e.chat_id, ids=e.id)
            return await e.client.send_message(e.chat_id, ok)
        except Exception as er:
            LOGS.info(er)


@ayra_cmd(pattern="listecho$")
async def lstecho(e):
    if k := list_echo(e.chat_id):
        user = "**Activated Echo For Users:**\n\n"
        for x in k:
            ok = await e.client.get_entity(int(x))
            kk = f"[{get_display_name(ok)}](tg://user?id={ok.id})"
            user += f"•{kk}" + "\n"
        await e.eor(user)
    else:
        await e.eor("`List is Empty, For echo`", time=5)
