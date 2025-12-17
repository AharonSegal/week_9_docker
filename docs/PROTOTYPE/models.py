from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    """
    Basic item model stored in the JSON database.
    """

    name: str
    description: Optional[str] = None
    price: float