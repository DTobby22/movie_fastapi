from pydantic import BaseModel, Field
from typing import Optional, List

class Movie(BaseModel):  # Esto es un schema
    id: Optional[int] = None
    title: str = Field(max_length=155, min_length=1)
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'example',
                'overview': 'example',
                'year': 2022,
                'rating': 2.5,
                'category': 'example'
            }
        }
