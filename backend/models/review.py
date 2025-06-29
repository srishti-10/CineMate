from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Review(BaseModel):
    user_id: str  # ID of the user who wrote the review
    movie_id: str  # ID of the movie being reviewed
    rating: int = Field(..., ge=1, le=5)  # Rating (1-5)
    review: Optional[str] = None  # Review text
    created_at: Optional[datetime] = None  # Timestamp 