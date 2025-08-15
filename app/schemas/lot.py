from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class LotStatus(str, Enum):
    RUNNING = "running"
    ENDED = "ended"


class LotCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    start_price: float = Field(..., gt=0)


class LotResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_price: float
    current_price: float
    status: LotStatus
    created_at: datetime
    ended_at: Optional[datetime]
    
    class Config:
        from_attributes = True