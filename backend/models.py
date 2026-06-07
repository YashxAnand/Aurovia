from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Pydantic Models ---

class UIComponent(BaseModel):
    type: str  # 'text', 'image', 'video'
    content: Optional[str] = None
    url: Optional[str] = None
    s3_key: Optional[str] = None

class PageData(BaseModel):
    page_name: str
    components: Dict[str, UIComponent]

class PageDataUpdate(BaseModel):
    components: Dict[str, UIComponent]

class BlogContentBlock(BaseModel):
    type: str # 'text' or 'image'
    content: Optional[str] = None
    url: Optional[str] = None
    s3_key: Optional[str] = None

class BlogPost(BaseModel):
    title: str
    slug: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    thumbnail: Optional[UIComponent] = None
    carousel_images: List[UIComponent] = []
    media_slots: List[UIComponent] = []
    text_blocks: List[str] = []

class PortfolioItem(BaseModel):
    type: str # 'image' or 'video'
    url: str
    s3_key: str
    title: str
    size_mb: Optional[float] = None
