import os
import json
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import bcrypt
from bson import ObjectId

from s3_client import upload_file_to_r2, delete_file_from_r2
from models import UIComponent, PageData, PageDataUpdate, BlogPost, BlogContentBlock, PortfolioItem

# Load environment variables
load_dotenv()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "aurovia_db"

app = FastAPI(title="Aurovia Website & Admin API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]
users_collection = db.users
pages_collection = db.pages
blogs_collection = db.blogs
portfolio_collection = db.portfolio

# Base Directory (Aurovia root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount Static Assets
app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(BASE_DIR, "js")), name="js")
app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")

# Templates Setup
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "backend", "templates"))

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

# Security Helper functions
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(username: str):
    user = await users_collection.find_one({"username": username})
    if user:
        return UserInDB(**user)
    return None

async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# ---------------------------------------------------------
# AUTHENTICATION API ROUTES
# ---------------------------------------------------------

@app.post("/api/login")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token", 
        value=access_token, 
        httponly=True, 
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

# ---------------------------------------------------------
# ADMIN CMS API ROUTES (Protected)
# ---------------------------------------------------------

@app.get("/api/admin/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_user_from_cookie)):
    return {
        "visitors": 1245,
        "inquiries": 12,
        "message": f"Welcome to the admin panel, {current_user.username}!"
    }

# --- Pages CMS ---
@app.get("/api/admin/pages")
async def get_all_pages(current_user: User = Depends(get_current_user_from_cookie)):
    pages = await pages_collection.find().to_list(100)
    for p in pages:
        p['_id'] = str(p['_id'])
    return pages

@app.get("/api/admin/pages/{page_name}")
async def get_page(page_name: str, current_user: User = Depends(get_current_user_from_cookie)):
    page = await pages_collection.find_one({"page_name": page_name})
    if not page:
        return {"page_name": page_name, "components": {}}
    page['_id'] = str(page['_id'])
    return page

@app.put("/api/admin/pages/{page_name}")
async def update_page(page_name: str, update: PageDataUpdate, current_user: User = Depends(get_current_user_from_cookie)):
    # Upsert the page data
    update_data = {"page_name": page_name, "components": {k: v.dict() for k, v in update.components.items()}}
    await pages_collection.update_one(
        {"page_name": page_name},
        {"$set": update_data},
        upsert=True
    )
    return {"message": "Page updated successfully"}

# --- Media Upload CMS ---
@app.post("/api/admin/upload")
async def upload_media(file: UploadFile = File(...), current_user: User = Depends(get_current_user_from_cookie)):
    # Enforce 300MB limit
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > 300 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 300MB limit")
        
    content_type = file.content_type
    key, url = upload_file_to_r2(file.file, file.filename, content_type)
    
    if not url:
        raise HTTPException(status_code=500, detail="Failed to upload file to S3")
        
    return {"url": url, "s3_key": key}

@app.delete("/api/admin/media")
async def delete_media(s3_key: str, current_user: User = Depends(get_current_user_from_cookie)):
    delete_file_from_r2(s3_key)
    return {"message": "Deleted successfully"}

# --- Blogs CMS ---
@app.get("/api/admin/blogs")
async def get_blogs_admin(current_user: User = Depends(get_current_user_from_cookie)):
    blogs = await blogs_collection.find().to_list(100)
    for b in blogs:
        b['_id'] = str(b['_id'])
    return blogs

@app.post("/api/admin/blogs")
async def create_blog(blog: BlogPost, current_user: User = Depends(get_current_user_from_cookie)):
    blog_dict = blog.dict()
    await blogs_collection.insert_one(blog_dict)
    return {"message": "Blog created successfully"}

@app.put("/api/admin/blogs/{slug}")
async def update_blog(slug: str, blog: BlogPost, current_user: User = Depends(get_current_user_from_cookie)):
    # Need to check old media to delete? Assuming client handles it.
    await blogs_collection.update_one({"slug": slug}, {"$set": blog.dict()})
    return {"message": "Blog updated successfully"}

@app.delete("/api/admin/blogs/{slug}")
async def delete_blog(slug: str, current_user: User = Depends(get_current_user_from_cookie)):
    # Find blog to delete media
    blog = await blogs_collection.find_one({"slug": slug})
    if blog:
        if blog.get("thumbnail") and blog["thumbnail"].get("s3_key"):
            delete_file_from_r2(blog["thumbnail"]["s3_key"])
        for block in blog.get("content_blocks", []):
            if block.get("s3_key"):
                delete_file_from_r2(block["s3_key"])
        await blogs_collection.delete_one({"slug": slug})
    return {"message": "Blog deleted successfully"}

# --- Portfolio CMS ---
@app.get("/api/admin/portfolio")
async def get_portfolio_admin(current_user: User = Depends(get_current_user_from_cookie)):
    items = await portfolio_collection.find().to_list(100)
    for i in items:
        i['_id'] = str(i['_id'])
    return items

@app.post("/api/admin/portfolio")
async def create_portfolio_item(item: PortfolioItem, current_user: User = Depends(get_current_user_from_cookie)):
    count = await portfolio_collection.count_documents({})
    if count >= 100:
        raise HTTPException(status_code=400, detail="Maximum limit of 100 portfolio items reached")
    await portfolio_collection.insert_one(item.dict())
    return {"message": "Portfolio item added"}

@app.delete("/api/admin/portfolio/{item_id}")
async def delete_portfolio_item(item_id: str, current_user: User = Depends(get_current_user_from_cookie)):
    item = await portfolio_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        if item.get("s3_key"):
            delete_file_from_r2(item["s3_key"])
        await portfolio_collection.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Item deleted"}

# ---------------------------------------------------------
# HTML PAGE SERVING (Frontend Routes)
# ---------------------------------------------------------

async def get_page_context(page_name: str, request: Request):
    page = await pages_collection.find_one({"page_name": page_name})
    components = page.get("components", {}) if page else {}
    return {"request": request, "components": components}

@app.get("/")
async def serve_home(request: Request):
    ctx = await get_page_context("home", request)
    return templates.TemplateResponse(request=request, name="index.html", context=ctx)

@app.get("/about-us")
async def serve_about(request: Request):
    ctx = await get_page_context("about-us", request)
    return templates.TemplateResponse(request=request, name="about-us.html", context=ctx)

@app.get("/portfolio")
async def serve_portfolio(request: Request):
    ctx = await get_page_context("portfolio", request)
    items = await portfolio_collection.find().to_list(100)
    ctx["portfolio_items"] = items
    return templates.TemplateResponse(request=request, name="portfolio.html", context=ctx)

@app.get("/services")
async def serve_services(request: Request):
    ctx = await get_page_context("services", request)
    return templates.TemplateResponse(request=request, name="services.html", context=ctx)

@app.get("/blogs")
async def serve_blogs(request: Request):
    ctx = await get_page_context("blogs", request)
    blogs = await blogs_collection.find().sort("created_at", -1).to_list(100)
    ctx["blogs"] = blogs
    return templates.TemplateResponse(request=request, name="blogs.html", context=ctx)

@app.get("/blog/{slug}")
async def serve_blog_single(request: Request, slug: str):
    blog = await blogs_collection.find_one({"slug": slug})
    if not blog:
        return templates.TemplateResponse(request=request, name="404.html", context={"request": request}, status_code=404)
    return templates.TemplateResponse(request=request, name="blog_single.html", context={"request": request, "blog": blog})

@app.get("/get-in-touch")
async def serve_contact(request: Request):
    ctx = await get_page_context("get-in-touch", request)
    return templates.TemplateResponse(request=request, name="get-in-touch.html", context=ctx)

# ---------------------------------------------------------
# ADMIN PAGE ROUTES (Protected)
# ---------------------------------------------------------

@app.get("/login")
@app.get("/admin/login")
async def serve_admin_login(request: Request):
    return FileResponse(os.path.join(BASE_DIR, "admin", "login.html"))

@app.get("/admin")
async def serve_admin(request: Request):
    return RedirectResponse(url="/admin/dashboard")

@app.get("/admin/dashboard")
async def serve_admin_dashboard(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/admin/login")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return RedirectResponse(url="/admin/login")
    except JWTError:
        return RedirectResponse(url="/admin/login")
        
    return FileResponse(os.path.join(BASE_DIR, "admin", "dashboard.html"))

# ---------------------------------------------------------
# CUSTOM 404 HANDLER & REDIRECTS
# ---------------------------------------------------------

@app.get("/{page_name}.html")
async def redirect_html_extension(page_name: str, request: Request):
    return RedirectResponse(url=f"/{page_name}")

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(request=request, name="404.html", context={"request": request}, status_code=404)
