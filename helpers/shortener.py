from shortzy import Shortzy
from mdisky import Mdisk
from config import MDISK_API, SHORTENER_API, SHORTENER_WEBSITE

shortzy = Shortzy(SHORTENER_API, SHORTENER_WEBSITE) if SHORTENER_API and SHORTENER_WEBSITE else None


async def mdisk_droplink_convertor(text):
    if MDISK_API:
        text = await mdisk_api_handler(text)
    if shortzy:
        text = await replace_link(text)
    return text

async def mdisk_api_handler(text):
    mdisk = Mdisk(MDISK_API)
    return await mdisk.convert_from_text(text)

async def replace_link(text):
    return await shortzy.convert_from_text(text)