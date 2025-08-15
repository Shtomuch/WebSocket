from pydantic import BaseModel, Field
from datetime import datetime


class BidCreate(BaseModel):
    bidder: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)


class BidResponse(BaseModel):
    id: int
    lot_id: int
    bidder: str
    amount: float
    created_at: datetime
    
    class Config:
        from_attributes = True