import re
from pyrogram import Client, filters, enums
from .database import collection
from bson.objectid import ObjectId
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.get_movie import get_movies, search_for_videos
from helpers.get_movie import BUTTONS
from helpers.auto_delete import auto_delete
from helpers.shortener import mdisk_droplink_convertor
import math
from pyrogram.errors import UserIsBlocked, PeerIdInvalid

@Client.on_callback_query(filters.regex(r"^send"))
async def cb_send_handler(c, m):
    id = m.data.split("#")[1]
    if m.message.chat.type == enums.ChatType.PRIVATE:
        result = await collection.find_one({"_id": ObjectId(id)})

        try:
            caption = result["caption"]
        except Exception as e:
            return await m.message.reply("Some error occurred")

        caption = await replace_username(caption)

        if m.message.chat.id in ADMINS:
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Delete", callback_data=f"delete#{id}")],
                ]
            )
        else:
            reply_markup = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("How To Download ❓", url=f"https://t.me/{HOWTO}")],
                ]
            )
        caption = await mdisk_droplink_convertor(caption)
        caption = CUSTOM_CAPTION.format(caption=caption)
        await m.message.reply_photo(
                caption=caption, photo=result["thumbnail"], reply_markup=reply_markup
            )
    
    elif m.message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        try:
            await m.answer(url=f'https://telegram.me/{c.raw_username}?start=send_{id}')
        except Exception as e:
            print(e)
            await m.answer("Some error occured", show_alert=True)
    

@Client.on_callback_query(filters.regex(r"^delete"))
async def cb_delete_handler(c, m):
    try:
        _id = m.data.split("#")[1]
        my_query = {"_id": ObjectId(_id)}
        await collection.delete_one(my_query)
        txt = await m.message.edit("Deleted Successfully")
    except Exception as e:
        print(e)
        txt = await m.message.edit("Some error occurred while deleting")
    await auto_delete(m.message, txt)


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


@Client.on_callback_query(filters.regex(r"^close"))
async def cb_close_handler(c, m):
    await m.answer()
    await m.message.delete()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def send_spell_checker(bot, query):
    print(query.data)
    _, user, movie_ = query.data.split("#")
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("Search for yourself", show_alert=True)

    results = await get_movies(movie_, query.message)
    if results is None:
        await query.answer("Movie not found in database", show_alert=True)

    await auto_delete(query.message, results)


# Next Button


@Client.on_callback_query(filters.regex(r"^next"))
async def next_btn_cb_handler(client: Client, query: CallbackQuery):
    txt = None
    print(query.data)
    ident, offset, keyword = query.data.split("_")

    list2 = []
    offset = int(offset) * 10
    results = await search_for_videos(keyword)
    if results is not None:
        for result in results[offset : offset + RESULTS_COUNT]:
            id = str(result["_id"])

            if query.message.chat.id in ADMINS:
                list2 += (
                    [
                        InlineKeyboardButton(
                            result["title"], callback_data=f"send#{id}"
                        ),
                        InlineKeyboardButton("Delete", callback_data=f"delete#{id}"),
                    ],
                )
            else:
                list2 += (
                    [
                        InlineKeyboardButton(
                            result["title"], callback_data=f"send#{id}"
                        ),
                    ],
                )

            if len(list2) >= RESULTS_COUNT:
                break

        list2.append(
            [
                InlineKeyboardButton(
                    text="BACK", callback_data=f"back_{int(offset/10)-1}_{keyword}"
                )
            ],
        )

        if int((offset / 10) + 1) < math.ceil(len(results) / 10):

            list2.append(
                [
                    InlineKeyboardButton(
                        text="NEXT ⏩",
                        callback_data=f"next_{int(offset/10)+1}_{keyword}",
                    )
                ],
            )

        list2.append(
            [
                InlineKeyboardButton(
                    text=f"📃 Pages {int((offset/10)+1)} / {math.ceil(len(results) / 10)}",
                    callback_data="pages",
                )
            ],
        )

        reply_markup = InlineKeyboardMarkup(list2)
        txt = await query.edit_message_caption(
            caption=f"Results for {keyword}", reply_markup=reply_markup
        )


# Back Button
@Client.on_callback_query(filters.regex(r"^back"))
async def back_btn_cb_handler(client: Client, query: CallbackQuery):
    txt = None
    ident, offset, keyword = query.data.split("_")

    list2 = []
    offset = int(offset) * 10
    results = await search_for_videos(keyword)
    if results is not None:
        for result in results[offset : offset + RESULTS_COUNT]:
            id = str(result["_id"])

            if query.message.chat.id in ADMINS:
                list2 += (
                    [
                        InlineKeyboardButton(
                            result["title"], callback_data=f"send#{id}"
                        ),
                        InlineKeyboardButton("Delete", callback_data=f"delete#{id}"),
                    ],
                )
            else:
                list2 += (
                    [
                        InlineKeyboardButton(
                            result["title"], callback_data=f"send#{id}"
                        ),
                    ],
                )

            if len(list2) >= RESULTS_COUNT:
                break

        list2.append(
            [
                InlineKeyboardButton(
                    text="NEXT ⏩", callback_data=f"next_{int(offset/10)+1}_{keyword}"
                )
            ],
        )

        if int((offset / 10) + 1) == 0:

            list2.append(
                [
                    InlineKeyboardButton(
                        text="BACK", callback_data=f"back_{int(offset/10)-1}_{keyword}"
                    )
                ],
            )

        list2.append(
            [
                InlineKeyboardButton(
                    text=f"📃 Pages {int((offset/10)+1)} / {math.ceil(len(results) / 10)}",
                    callback_data="pages",
                )
            ],
        )

        reply_markup = InlineKeyboardMarkup(list2)
        txt = await query.edit_message_caption(
            caption=f"Results for {keyword}", reply_markup=reply_markup
        )
