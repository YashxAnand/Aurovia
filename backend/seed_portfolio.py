import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["aurovia_db"]

images = [
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-14.jpeg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-3.jpeg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-2.jpeg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-6.jpeg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-4.jpeg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-21.jpg",
    "assets/uploads/services/service-weddings.jpg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-9.jpg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-15.jpg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-7.jpg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-10.jpg",
    "assets/uploads/portfolio/gallery/big/portfolio-gallery-18.jpg"
]

async def seed_portfolio():
    # Only seed if collection is empty
    count = await db.portfolio.count_documents({})
    if count == 0:
        docs = []
        for i, url in enumerate(images):
            docs.append({
                "type": "image",
                "url": url,
                "s3_key": "",
                "title": f"Portfolio Image {i+1}",
                "size_mb": 0.0
            })
        await db.portfolio.insert_many(docs)
        print("Portfolio seeded successfully!")
    else:
        print("Portfolio already has items. Not seeding.")

asyncio.run(seed_portfolio())
