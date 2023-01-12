import re
from translation import *
from config import UPDATE_CHANNEL, WELCOME_IMAGE, FORCESUB
from pyrogram import Client, filters
from plugins.database import collection
from plugins.forcesub import forcesub_handler 
from pymongo import TEXT
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from helpers.shortener import mdisk_droplink_convertor
from config import *
from .database import collection
from bson.objectid import ObjectId

@Client.on_message(filters.command('start'))
async def start_message(c,m):
    
    collection.create_index([("title" , TEXT),("caption", TEXT)],name="movie_index")
    if len(m.command) == 1:
        return await m.reply_photo(WELCOME_IMAGE,
            caption=START_MESSAGE.format(m.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Our Channel", url=f'https://t.me/{USERNAME}')
                    ]
                ]
            )
        )
    if FORCESUB == 'True' and not await forcesub_handler(c, m):
        return
    try:
        id = m.command[1].split("_")[1]

        result = await collection.find_one({"_id": ObjectId(id)})

        try:
            caption = result["caption"]
        except Exception as e:
            return await m.reply("Some error occurred")

        caption = await replace_username(caption)

        reply_markup = (
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Delete", callback_data=f"delete#{id}"
                        )
                    ],
                ]
            )
            if m.chat.id in ADMINS
            else InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Join", url=f"https://t.me/{USERNAME}"
                        )
                    ],
                ]
            )
        )
        caption = await mdisk_droplink_convertor(caption)
        caption = CUSTOM_CAPTION.format(caption=caption)
        await m.reply_photo(
                caption=caption, photo=result["thumbnail"], reply_markup=reply_markup
            )
    except Exception as e:
        await m.reply(e)
        print(e)


async def replace_username(text):
    usernames = re.findall("([@#][A-Za-z0-9_]+)", text)

    for i in usernames:
        text = text.replace(i, f"@{USERNAME}")

    telegram_links = re.findall(
        r"[(?:http|https)?://]*(?:t.me|telegram.me)[^\s]+", text
    )

    for i in telegram_links:
        text = text.replace(i, f"@{USERNAME}")

    return text