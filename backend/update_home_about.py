import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["aurovia_db"]

async def update_pages():
    home_components = {
        "about_image": {"type": "image", "url": "assets/front/assets/images/about-section-showcase.jpg"},
        "home_subtitle": {"type": "text", "content": "“9+ Years, 1000+ Smiles — And Counting!”"},
        "home_about_content": {"type": "text", "content": "<p>From candid chuckles to tear-jerking vows, our passionate team at Aurovia has mastered the art of wedding magic through lens and heart.</p><p>At Aurovia, wedding photography isn't just a business—it is our joyful obsession! For over nine years, our camera-wielding superheroes have leapt across banquet halls and scenic gardens, capturing everything from wild baraat dance-offs to whispered rooftop vows.</p>"},
        "service_image_1": {"type": "image", "url": "assets/uploads/services/service-weddings.jpg"},
        "service_image_2": {"type": "image", "url": "assets/uploads/services/service-pre-wedding.jpg"},
        "service_image_3": {"type": "image", "url": "assets/uploads/services/service-engagements.jpg"},
        "service_image_4": {"type": "image", "url": "assets/uploads/services/service-parties-birthdays.jpg"},
        "signature_bg": {"type": "image", "url": "assets/front/assets/images/signature-style-bg.jpg"}
    }
    
    for key, val in home_components.items():
        await db.pages.update_one(
            {"page_name": "home"},
            {"$set": {f"components.{key}": val}},
            upsert=True
        )
        
    about_components = {
        "about_image": {"type": "image", "url": "assets/uploads/services/service-weddings.jpg"}
    }
    
    for key, val in about_components.items():
        await db.pages.update_one(
            {"page_name": "about-us"},
            {"$set": {f"components.{key}": val}},
            upsert=True
        )
    
    print("Database pages updated successfully!")

asyncio.run(update_pages())
