import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["aurovia_db"]

async def seed():
    pages = [
        {
            "page_name": "home",
            "components": {
                "hero_title": {"type": "text", "content": "Creating Timeless Memories<br><i>with</i> Aurovia"},
                "hero_video": {"type": "video", "url": "https://media.auroviaweddings.com/home-hero-bg.mp4"},
                "about_text": {"type": "text", "content": "Aurovia Productions captures the magic of your special day with breathtaking photography and cinematic storytelling."}
            }
        },
        {
            "page_name": "about-us",
            "components": {
                "hero_title": {"type": "text", "content": "Our Story"},
                "hero_video": {"type": "video", "url": "https://media.auroviaweddings.com/about-hero-bg.mp4"},
                "about_content": {"type": "text", "content": "We are a team of passionate storytellers dedicated to preserving your most precious moments."}
            }
        },
        {
            "page_name": "services",
            "components": {
                "hero_title": {"type": "text", "content": "Our Services"},
                "hero_video": {"type": "video", "url": "https://media.auroviaweddings.com/services-hero-bg.mp4"},
                "services_intro": {"type": "text", "content": "From intimate gatherings to grand celebrations, we offer comprehensive coverage."}
            }
        },
        {
            "page_name": "get-in-touch",
            "components": {
                "hero_title": {"type": "text", "content": "Get In Touch"},
                "contact_intro": {"type": "text", "content": "Let's create something beautiful together. Reach out to us for bookings and inquiries."}
            }
        }
    ]
    
    for p in pages:
        await db.pages.update_one({"page_name": p["page_name"]}, {"$setOnInsert": p}, upsert=True)
    
    print("Database seeded successfully!")

asyncio.run(seed())
