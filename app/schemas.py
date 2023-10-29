from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Price(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    gid: int
    amount: float = None
    product_gid: int
    created: datetime
    

class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    gid: int
    name: str = None
    url: str = None
    prices: List[Price]
    created: datetime
    last_updated: datetime
    
