import asyncio
import os
import requests
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def setup_admin_and_update_blog():
    # Setup admin directly in DB so we know the credentials
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client["aurovia_db"]
    users = db["users"]
    
    username = "test_admin"
    password = "test_password"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    await users.update_one(
        {"username": username},
        {"$set": {"username": username, "hashed_password": hashed}},
        upsert=True
    )
    
    # Now use the API with the known credentials
    session = requests.Session()
    login_res = session.post(
        "http://127.0.0.1:8000/api/login",
        data={"username": username, "password": password}
    )
    if login_res.status_code != 200:
        print("Login failed!", login_res.text)
        return

        
    # 2. Fetch all blogs to find the Varanasi one
    blogs_res = session.get("http://127.0.0.1:8000/api/admin/blogs")
    blogs = blogs_res.json()
    target_slug = "december-wedding-varanasi-2025"
    
    target_blog = None
    for b in blogs:
        if b.get("slug") == target_slug:
            target_blog = b
            break
            
    if not target_blog:
        print("Blog not found!")
        return
        
    # 3. Update Text Blocks with rich HTML (Times New Roman, large text, italics)
    target_blog["text_blocks"] = [
        "<p><span style=\"font-family: 'Times New Roman', Times, serif; font-size: 1.5em;\"><strong>A Magical Winter in Varanasi</strong></span></p><p><span style=\"font-family: 'Times New Roman', Times, serif; font-size: 1.25em;\">Varanasi in December is nothing short of magical. The misty mornings over the Ganges, the chants echoing through the ghats, and the vibrant colors of a traditional Indian wedding create an atmosphere that is deeply <em>spiritual</em> and profoundly <em>romantic</em>. This was the setting for Ananya and Rohan’s breathtaking wedding, a celebration we at Aurovia were honored to capture.</span></p>",
        
        "<p><span style=\"font-family: 'Times New Roman', Times, serif; font-size: 1.25em;\">The festivities kicked off with a vibrant Haldi ceremony by the riverbanks. The golden hues of turmeric matched the warm winter sun perfectly. Surrounded by their closest family and friends, the couple's joy was palpable. Our team focused on capturing the candid moments—the uncontrollable laughter, the tearful hugs, and the sheer exuberance of the day. <em>It was a visual feast of emotion and color.</em> Every smile and every tear was beautifully illuminated by the setting winter sun.</span></p>",
        
        "<p><span style=\"font-family: 'Times New Roman', Times, serif; font-size: 1.25em;\">As the sun set, the city transformed. The evening Sangeet was a spectacular affair with energetic performances that kept everyone on their toes. But the highlight was undoubtedly the wedding day itself. Against the backdrop of an ancient temple, Ananya and Rohan exchanged their vows. The timeless architecture of Varanasi combined with the profound emotion of the moment made for some of our favorite shots of the year. <strong>Here's to love, laughter, and a happily ever after!</strong> We hope these glimpses convey the profound beauty of their unforgettable union.</span></p>"
    ]
    
    # 4. PUT updated blog using API
    put_res = session.put(
        f"http://127.0.0.1:8000/api/admin/blogs/{target_slug}",
        json=target_blog
    )
    
    if put_res.status_code == 200:
        print("Successfully updated blog via API:", put_res.json())
    else:
        print("Failed to update blog via API:", put_res.status_code, put_res.text)

if __name__ == "__main__":
    asyncio.run(setup_admin_and_update_blog())
