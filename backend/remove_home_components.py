import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["aurovia_db"]

async def remove_components():
    await db.pages.update_one(
        {"page_name": "home"},
        {"$unset": {
            "components.hero_title": "",
            "components.about_text": ""
        }}
    )
    print("Components removed from home page successfully!")

asyncio.run(remove_components())
