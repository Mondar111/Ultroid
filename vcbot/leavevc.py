# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from . import *


@asst_cmd(f"(leave|leave@{vcusername})",
          from_users=VC_AUTHS()
)
async def leavehandler(message):
    spli = message.text.split(" ", maxsplit=1)
    try:
        chat = (await Client.get_chat(spli[1])).id
    except IndexError:
        chat = get_chat_id(message)
    except Exception as Ex:
        return await eor(message, str(Ex))
    CallsClient.leave_group_call(chat)
    m = await eor(message, "Successfully Left Group Call..")
    try:
        QUEUE.pop(chat)
    except KeyError:
        pass
    await asyncio.sleep(5)
    await m.delete()


@Client.on_message(filters.me & filters.command("leavevc", HNDLR) & ~filters.edited)
async def lhandler(_, message):
    await leavehandler(message)
