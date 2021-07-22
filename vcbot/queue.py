# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from . import *


@asst_cmd(
    f"(clearqueue|clearqueue@{vcusername})",
    from_users=VC_AUTHS()
)
async def clear_queue(message):
    chat_id = get_chat_id(message)
    try:
        QUEUE.pop(chat_id)
    except KeyError:
        return await eor(message, "Queue Not Found !")
    # Todo - Clear Remaining Songs
    return await eor(message, "Cleared Queue...")


@Client.on_message(
    filters.outgoing & filters.command("clearqueue", HNDLR) & ~filters.edited
)
async def clearqueue_vc(_, message):
    await clear_queue(message)


@asst_cmd(
    f"(queue|queue@{vcusername})",
    from_users=VC_AUTHS()
)
async def queuee(event):
    mst = event.text.split(" ", maxsplit=1)
    try:
        chat = (await Client.get_chat(mst[1])).id
    except BaseException:
        chat = get_chat_id(event)
    txt = list_queue(chat)
    if txt:
        return await eor(event, txt)
    await eor(event, "No Queue Found !")


@Client.on_message(filters.outgoing & filters.command("queue", HNDLR) & ~filters.edited)
async def queue_vc(_, message):
    await queuee(message)
