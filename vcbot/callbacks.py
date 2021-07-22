# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import re
from . import *
from .play import queue_func


@callback(re.compile("^vc(.*)"))
async def stopresumevc(event):
    if event.sender_id not in VC_AUTHS():
        return await event.answer(
            "You are Not Authorised to Use Me !"
        )
    match = event.pattern_match.group(1).split("_")
    chat = int(match[1])
    if match[0] == "r":
        CallsClient.resume_stream(chat)
        BT = "Pause"
    else:
        CallsClient.pause_stream(chat)
        BT = "Resume"
    await event.answer("Done", alert=True)
    dt = BT[0].lower()
    await event.edit(buttons=Button.inline(
        BT, 
        data=f"vc{dt}_{chat}")
    )



@callback(re.compile("^skip_(.*)"))
async def skipstream(event):
    if event.sender_id not in VC_AUTHS():
        return await event.answer(
            "You are Not Authorised to Use Me !"
        )
    match = event.pattern_match.group(1)
    await event.answer("Skipped !", alert=True)
    await event.delete()
    await queue_func(int(match))


@callback(re.compile("^ex_(.*)"))
async def exit_vc(event):
    if event.sender_id not in VC_AUTHS():
        return await event.answer(
            "You are Not Authorised to Use Me !"
    )
    match = event.pattern_match.group(1)
    if int(match) not in CallsClient.active_calls.keys():
        return await event.delete()
    QUEUE.pop(int(match))
    CallsClient.leave_group_call(int(match))
    await event.answer("Exited !", alert=True)
    await event.delete()
