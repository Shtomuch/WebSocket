from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class LotStatus(str, enum.Enum):
    RUNNING = "running"
    ENDED = "ended"


class Lot(Base):
    __tablename__ = "lots"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    start_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    status = Column(Enum(LotStatus), default=LotStatus.RUNNING, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    

    bids = relationship("Bid", back_populates="lot", cascade="all, delete-orphan")