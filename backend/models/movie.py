from pydantic import BaseModel, Field
from typing import List, Optional

class Movie(BaseModel):
    title: str  # Movie title
    year: int  # Release year
    genres: List[str]  # List of genres
    description: Optional[str] = None  # Movie description
    director: Optional[str] = None  # Director's name
    cast: List[str] = []  # List of cast members
    poster_url: Optional[str] = None  # Link to poster image
    avg_rating: Optional[float] = 0.0  # Average rating
    num_reviews: Optional[int] = 0  # Number of reviews 