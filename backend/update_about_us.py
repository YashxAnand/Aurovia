import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["aurovia_db"]

async def seed_about_us():
    components = {
        "hero_title": {"type": "text", "content": "Our Story"},
        "hero_subtitle": {"type": "text", "content": "“9+ Years, 1000+ Smiles — And Counting!”"},
        "about_content": {"type": "text", "content": "<p>At Aurovia, wedding photography isn't just a business—it is our joyful obsession! For over nine years, our camera-wielding superheroes have leapt across banquet halls and scenic gardens, capturing everything from wild baraat dance-offs to whispered rooftop vows. We believe every love story is a new adventure, deserving a team that is equal parts artistic and fun (with just the right pinch of professional mischief).</p><p>Our journey began with a simple wish: freeze fleeting smiles and laughter so they can be cherished forever.</p>"}
    }
    
    # We update the about-us page components
    # We'll merge them in so we don't lose hero_video if it's there, but wait, it's safer to just set them.
    for key, val in components.items():
        await db.pages.update_one(
            {"page_name": "about-us"},
            {"$set": {f"components.{key}": val}},
            upsert=True
        )
    
    print("About Us updated successfully!")

asyncio.run(seed_about_us())
