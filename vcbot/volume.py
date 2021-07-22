# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from pyrogram.raw import functions

from . import *


@asst_cmd(
    f"(volume|volume@{vcusername})$",
    from_users=VC_AUTHS()
)
async def chesendvolume(message):
    mk = message.text.split(" ")
    chat_id = get_chat_id(message)
    if not len(mk) > 1:
        me = await Client.get_me()
        fchat = await Client.send(
            functions.channels.GetFullChannel(
                channel=await Client.resolve_peer(chat_id)
            )
        )
        mk = fchat.full_chat.call
        Vl = await Client.send(
            functions.phone.GetGroupParticipants(
                call=mk,
                ids=[await Client.resolve_peer(me.id)],
                sources=[],
                offset="",
                limit=0,
            )
        )
        try:
            CML = Vl.participants[0].volume
        except IndexError:
            CML = 0
        return await eor(message, f"**Current Volume :** {CML}%")
    try:
        if int(mk[1]) not in range(0, 201):
            return await eor(message, "`Volume` should be in between `0-200`")
        CallsClient.change_volume_call(chat_id, int(mk[1]))
        msg = f"Volume Changed to `{mk[1]}%`"
    except Exception as msg:
        msg = str(msg)
    await eor(message, msg)


@Client.on_message(filters.me & filters.command("volume", HNDLR) & ~filters.edited)
async def volplay(_, message):
    await chesendvolume(message)
