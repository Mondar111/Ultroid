# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from . import *
from .play import queue_func


@asst_cmd(
    f"(skip|skip@{vcusername})$",
    from_users=VC_AUTHS()
)
async def skiplife(message):
    mst = message.text.split(" ", maxsplit=1)
    try:
        chat = (await Client.get_chat(mst[1])).id
    except BaseException:
        chat = get_chat_id(message)
    await queue_func(chat)


@Client.on_message(
    filters.command("skip", HNDLR)
    & filters.outgoing
    & ~filters.edited
    & ~filters.forwarded
)
async def vc_skipe(_, message):
    await skiplife(message)
