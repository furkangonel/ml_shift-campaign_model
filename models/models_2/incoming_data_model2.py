from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    product: str
    price: float
    profit_margin: float
    quantity: int


class IncomingData_Model2(BaseModel):
    order_id: int
    products: List[Product]