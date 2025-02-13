from pydantic import BaseModel
from typing import List, Optional


class CampaignRequest(BaseModel):
    order_id: Optional[str]
    first_product: str
    second_product: str
    first_price: float
    second_price: float
    first_profit_margin: float
    second_proft_margin: float
    total_price: float
    discount: float
    label: int