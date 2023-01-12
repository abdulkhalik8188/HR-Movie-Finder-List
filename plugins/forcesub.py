import base64
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import FORCESUB, UPDATE_CHANNEL, OWNER_ID

@Client.on_message(filters.private & filters.incoming)
async def forcesub(c, m):
    if FORCESUB == 'True' and not await forcesub_handler(c, m):
        return
    await m.continue_propagation()



async def forcesub_handler(c,m):

    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "kicked":
                await m.reply_text("**Hey you are banned 😜**", quote=True)
                return
        except UserNotParticipant:
            invite_link = await c.create_chat_invite_link(UPDATE_CHANNEL)
            buttons = [[InlineKeyboardButton(text='Updates Channel 🔖', url=invite_link.invite_link)]]

            await m.reply_text(
                f"Hey {m.from_user.mention(style='md')} you need join My updates channel in order to use me 😉\n\n"
                "__Press the Following Button to join Now 👇__",
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
            return
        except Exception as e:
            print(e)
            await m.reply_text(f"Something Wrong. Please try again later or contact {owner.mention(style='md')}", quote=True)
            return

    return True

    


