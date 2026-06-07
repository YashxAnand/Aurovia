import os
import random
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def publish_test_blog():
    MONGODB_URL = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client["aurovia_db"]
    portfolio = db.portfolio
    
    # Fetch 7 random images
    items = await portfolio.aggregate([{"$match": {"type": "image"}}, {"$sample": {"size": 7}}]).to_list(length=7)
    
    if len(items) < 7:
        print("Not enough portfolio items to pick 7 random photos.")
        return

    # Extract exactly 4 for carousel
    carousel_images = []
    for i in range(4):
        carousel_images.append({
            "type": "image",
            "url": items[i]["url"],
            "s3_key": items[i]["s3_key"]
        })
    
    # Extract 3 for media slots
    media_slots = []
    for i in range(4, 7):
        media_slots.append({
            "type": "image",
            "url": items[i]["url"],
            "s3_key": items[i]["s3_key"]
        })

    # Text blocks
    text_blocks = [
        "<h2>A Magical Winter in Varanasi</h2><p>Varanasi in December is nothing short of magical. The misty mornings over the Ganges, the chants echoing through the ghats, and the vibrant colors of a traditional Indian wedding create an atmosphere that is deeply spiritual and profoundly romantic. This was the setting for Ananya and Rohan’s breathtaking wedding, a celebration we at Aurovia were honored to capture.</p>",
        "<p>The festivities kicked off with a vibrant Haldi ceremony by the riverbanks. The golden hues of turmeric matched the warm winter sun perfectly. Surrounded by their closest family and friends, the couple's joy was palpable. Our team focused on capturing the candid moments—the uncontrollable laughter, the tearful hugs, and the sheer exuberance of the day.</p>",
        "<p>As the sun set, the city transformed. The evening Sangeet was a spectacular affair with energetic performances that kept everyone on their toes. But the highlight was undoubtedly the wedding day itself. Against the backdrop of an ancient temple, Ananya and Rohan exchanged their vows. The timeless architecture of Varanasi combined with the profound emotion of the moment made for some of our favorite shots of the year. Here's to love, laughter, and a happily ever after!</p>"
    ]

    # Construct the blog object
    blog_data = {
        "title": "A December to Remember: Wedding in Varanasi",
        "slug": "december-wedding-varanasi-2025",
        "carousel_images": carousel_images,
        "media_slots": media_slots,
        "text_blocks": text_blocks
    }

    # Since we can't easily fetch via HTTP with auth cookie here without logging in via the API, 
    # we'll insert directly into the database!
    blogs = db.blogs
    
    # Remove if exists
    await blogs.delete_one({"slug": "december-wedding-varanasi-2025"})
    
    # Insert
    blog_data["created_at"] = datetime.utcnow()
    await blogs.insert_one(blog_data)
    
    print("Test blog published successfully! View it at: http://127.0.0.1:8000/blog/december-wedding-varanasi-2025")

if __name__ == "__main__":
    asyncio.run(publish_test_blog())
