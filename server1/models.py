from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    quantity: int

