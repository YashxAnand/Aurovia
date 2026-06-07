import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client['aurovia_db']

async def run():
    print("Pages:", await db.pages.find().to_list(10))
    print("Blogs:", await db.blogs.find().to_list(10))

asyncio.run(run())
