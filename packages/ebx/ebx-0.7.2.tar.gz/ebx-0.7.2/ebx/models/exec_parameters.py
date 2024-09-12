from pydantic import BaseModel
from typing import Optional

class Config(BaseModel):
    max_pixels: Optional[int] = None
    scale: Optional[int] = None
    best_effort: Optional[bool] = None