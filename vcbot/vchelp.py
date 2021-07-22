# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from . import *

HELP_TEXT = "**View All Vc Commands Here :**\nhttps://telegra.ph/Vc-Commands-07-17-2"


@asst_cmd(
    f"(vchelp|vchelp@{vcusername})$",
    from_users=VC_AUTHS()
)
async def pass_it(message):
    await eor(message, HELP_TEXT)


@Client.on_message(
    filters.command("vchelp", HNDLR)
    & filters.outgoing
    & ~(filters.edited | filters.forwarded)
)
async def always(_, message):
    await eor(message, HELP_TEXT)
