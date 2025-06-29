from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    username: str  # Unique username
    email: EmailStr  # User's email address
    password: str  # Plain password for registration (not stored in DB)
    bio: Optional[str] = None  # Short user bio
    avatar_url: Optional[str] = None  # Link to avatar image
    bookmarks: List[str] = []  # List of Movie IDs (as strings)
    joined_at: Optional[datetime] = None  # Date user joined

class UserInDB(User):
    password_hash: str  # Hashed password (stored in DB)
    password: Optional[str] = None  # Exclude plain password from DB 