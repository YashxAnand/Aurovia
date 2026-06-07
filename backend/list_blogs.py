import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def get_blogs():
    MONGODB_URL = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client["aurovia_db"]
    blogs = await db.blogs.find().to_list(100)
    for b in blogs:
        print(b['slug'], b['title'])

if __name__ == "__main__":
    asyncio.run(get_blogs())
