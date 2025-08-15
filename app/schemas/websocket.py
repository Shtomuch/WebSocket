from pydantic import BaseModel
from enum import Enum
from typing import Any, Optional


class WebSocketMessageType(str, Enum):
    BID_PLACED = "bid_placed"
    LOT_ENDED = "lot_ended"
    CONNECTION_ESTABLISHED = "connection_established"
    ERROR = "error"


class WebSocketMessage(BaseModel):
    type: WebSocketMessageType
    lot_id: Optional[int] = None
    bidder: Optional[str] = None
    amount: Optional[float] = None
    message: Optional[str] = None
    data: Optional[Any] = None