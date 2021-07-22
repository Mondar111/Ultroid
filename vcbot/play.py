# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import asyncio
import os
import random

from . import *


@asst_cmd(
    f"(play|play@{vcusername})",
    from_users=VC_AUTHS()
)
async def startup(event):
    msg = await eor(event, get_string("com_1"))
    song = event.text.split(" ", maxsplit=1)
    reply = await event.get_reply_message()

    if len(song) > 1 and song[1].startswith("@" or "-"):
        song = song[1].split(" ", maxsplit=1)
        chat = await Client.get_chat(song[0])
    else:
        chat = await Client.get_chat(get_chat_id(event))

    thumb, med, song_name = None, None, ""
    TS = dt.now().strftime("%H:%M:%S")
    if not reply and len(song) > 1:
        song, thumb, song_name, duration = await download(msg, song[1], chat.id, TS)
    elif reply and reply.media:
        if mediainfo(reply.media) not in ["video", "audio"]:
            return await msg.edit("Reply to Audio File or Give Query to Search..")
        try:
            thumb = await reply.download_media(thumb=-1)
            med = reply.file
        except TypeError:
            pass
        dl = await reply.download_media()
        duration = med.duration
        song = f"VCSONG_{chat.id}_{TS}.raw"
        await bash(
            f'ffmpeg -i "{dl}" -f s16le -ac 1 -acodec pcm_s16le -ar 48000 {song} -y'
        )
    else:
        return await msg.edit("Reply to Audio File or Give Query to Search..")
    from_user = make_mention(event.sender if hasattr(event, "sender") else event.from_user)
    if chat.id in CallsClient.active_calls.keys():
        add_to_queue(chat.id, song, song_name, from_user, duration)
        return await msg.edit(
            f"Added **{song_name}** to queue at #{list(QUEUE[chat.id].keys())[-1]}"
        )
    che = await vc_check(chat.id, chat.type)
    if not che:
        try:
            Up = await Client.send(
                functions.phone.CreateGroupCall(
                    peer=await Client.resolve_peer(chat.id),
                    random_id=random.randrange(1, 100),
                )
            )
        except Exception as E:
            return await msg.edit(str(E))
    if thumb:
        await msg.delete()
        msg = await reply_photo(
            thumb,
            caption=f"🎸 **Playing :** {song_name}\n**☘ Duration :** {time_formatter(duration*1000)}\n👤 **Requested By :** {from_user}",
            buttons=reply_markup(chat.id),
        )
        if os.path.exists(thumb):
            os.remove(thumb)
    try:
        CallsClient.join_group_call(chat.id, song)
    except Exception as E:
        return await msg.edit(str(E))
    CH = await asst.send_message(
        LOG_CHANNEL, f"Joined Voice Call in {chat.title} [`{chat.id}`]"
    )
    await asyncio.sleep(duration)
    os.remove(song)
    await msg.delete()
    await CH.delete()


@Client.on_message(filters.me & filters.command(["play"], HNDLR) & ~filters.edited)
async def cstartup(_, message):
    await startup(message)


async def queue_func(chat_id: int):
    try:
        song, title, from_user, pos, dur = get_from_queue(chat_id)
        CallsClient.change_stream(chat_id, song)
      # CallsClient._add_active_call(chat_id)
        xx = await asst.send_message(
            chat_id,
            f"**Playing :** {title}\n**Duration** : {time_formatter(dur*1000)}\n**Requested by**: {from_user}",
            buttons=reply_markup(chat_id),
        )
        QUEUE[chat_id].pop(pos)
        if not QUEUE[chat_id]:
            QUEUE.pop(chat_id)
        await asyncio.sleep(dur + 5)
      # CallsClient._remove_active_call(chat_id)
        await xx.delete()
    except (IndexError, KeyError):
        CallsClient.leave_group_call(chat_id)
    except Exception as ap:
        await asst.send_message(chat_id, f"`{str(ap)}`")


@CallsClient.on_stream_end()
async def streamhandler(chat_id: int):
    await queue_func(chat_id)
