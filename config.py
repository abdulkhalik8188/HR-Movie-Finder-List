import os

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OWNER_ID = int(os.environ.get("OWNER_ID"))
ADMINS = (
    [int(i) for i in os.environ.get("ADMINS", "").split(" ")]
    if os.environ.get("ADMINS")
    else []
)
if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)
MONGODB = os.environ.get('MONGODB')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME')
CHANNELS = os.environ.get('CHANNELS', "False")
CHANNELS_LIST = (
    [int(i) for i in os.environ.get("CHANNELS_LIST").split(" ")]
    if os.environ.get("CHANNELS_LIST")
    else []
)
FORCESUB = os.environ.get('FORCESUB', "True")

# Other Settings
UPDATE_CHANNEL =  int(os.environ.get('UPDATE_CHANNEL'))
USERNAME = os.environ.get('USERNAME')
HOWTO = os.environ.get('HOWTO', 'http://example.com')
RESULTS_COUNT = int(os.environ.get('RESULT_COUNTS', 10))
AUTO_DELETE = os.environ.get('AUTO_DELETE', False)
AUTO_DELETE_TIME = int(os.environ.get('AUTO_DELETE_TIME', 300))
IMDB_TEMPLATE = os.environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌‌‌‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
MAX_LIST_ELM = os.environ.get("MAX_LIST_ELM", None)
WELCOME_IMAGE = os.environ.get('WELCOME_IMAGE', 'https://bit.ly/3y8miWu')
RESULTS_IMAGE = os.environ.get('RESULTS_IMAGE', 'https://static.wikia.nocookie.net/ideas/images/e/e4/Movie_night.jpg')
MDISK_API=os.environ.get('MDISK_API')
SHORTENER_API=os.environ.get('SHORTENER_API')
SHORTENER_WEBSITE=os.environ.get('SHORTENER_WEBSITE')
OMDB_API=os.environ.get('OMDB_API')
CUSTOM_CAPTION=os.environ.get('CUSTOM_CAPTION', '{caption}')
#  Replit Config
REPLIT_USERNAME = os.environ.get("REPLIT_USERNAME", None)
REPLIT_APP_NAME = os.environ.get("REPLIT_APP_NAME", None)
REPLIT = f"https://{REPLIT_APP_NAME.lower()}.{REPLIT_USERNAME}.repl.co" if REPLIT_APP_NAME and REPLIT_USERNAME else False
PING_INTERVAL = int(os.environ.get("PING_INTERVAL", "300"))
USE_OMDB = os.environ.get("USE_OMDB", False)
