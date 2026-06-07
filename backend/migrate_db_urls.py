import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["aurovia_db"]

def extract_filename(url):
    if not url: return url
    return url.split("/")[-1]

async def migrate_db():
    # 1. Migrate Portfolio
    portfolio_items = await db.portfolio.find().to_list(1000)
    for item in portfolio_items:
        if "assets/" in item.get("url", ""):
            filename = extract_filename(item["url"])
            new_url = f"https://media.auroviaweddings.com/{filename}"
            await db.portfolio.update_one(
                {"_id": item["_id"]},
                {"$set": {"url": new_url}}
            )
            print(f"Updated portfolio item {item['_id']} to {new_url}")

    # 2. Migrate Pages components
    pages = await db.pages.find().to_list(100)
    for page in pages:
        components = page.get("components", {})
        updated = False
        for key, comp in components.items():
            if comp.get("type") in ["image", "video"] and "assets/" in comp.get("url", ""):
                filename = extract_filename(comp["url"])
                comp["url"] = f"https://media.auroviaweddings.com/{filename}"
                updated = True
        if updated:
            await db.pages.update_one(
                {"_id": page["_id"]},
                {"$set": {"components": components}}
            )
            print(f"Updated page {page['page_name']}")

    print("Database migration complete.")

if __name__ == "__main__":
    asyncio.run(migrate_db())
