from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):  # Esto es un esquema
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str
