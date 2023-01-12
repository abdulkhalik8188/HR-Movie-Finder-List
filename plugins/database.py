from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB, DATABASE_NAME, COLLECTION_NAME

client = AsyncIOMotorClient(MONGODB)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


async def add_file(unique_id, caption, title, thumbnail):
    res = {
        "caption": caption,
        "title": title,
        "unique_id": unique_id,
        "thumbnail": thumbnail,
    }
    already_exist = await collection.find_one({"unique_id": unique_id, "caption": caption})
    if not already_exist:
        return await collection.insert_one(res)
