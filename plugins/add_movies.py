
from pyrogram import Client, filters
from pyrogram.types import Message
from .database import add_file
from config import ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Add Movie to database
@Client.on_message(filters.user(ADMINS) & filters.media & filters.private)
async def web_db(c: Client, m: Message):
    if m.caption and m.photo:
        message = m.caption

        res = {
            "caption": message.html,
            "title": message.splitlines()[0],
            "thumbnail": m.photo.file_id,
            "unique_id": m.photo.file_unique_id,
        }
        _id = await add_file(**res)

        if not _id:
            await m.reply("This file already exists")
            return

        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Delete", callback_data=f"delete#{_id.inserted_id }"
                    )
                ],
            ]
        )

        await m.reply("Added Successfully", reply_markup=reply_markup)

    else:
        await m.reply("Something went wrong")
