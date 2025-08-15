from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Bid, Lot
from app.models.lot import LotStatus
from app.schemas.bid import BidCreate
from app.services.lot_service import LotService


class BidService:
    @staticmethod
    async def place_bid(db: AsyncSession, lot_id: int, bid_data: BidCreate) -> Optional[Bid]:
        """Place a bid on a lot"""
        # Check if lot exists and is running
        lot = await LotService.get_lot(db, lot_id)
        if not lot or lot.status != LotStatus.RUNNING:
            return None
        
        # Validate bid amount is higher than current price
        if bid_data.amount <= lot.current_price:
            raise ValueError(f"Bid amount must be higher than current price: {lot.current_price}")
        
        # Create bid
        bid = Bid(
            lot_id=lot_id,
            bidder=bid_data.bidder,
            amount=bid_data.amount
        )
        db.add(bid)
        
        # Update lot's current price
        lot.current_price = bid_data.amount
        
        await db.commit()
        await db.refresh(bid)
        return bid
    
    @staticmethod
    async def get_lot_bids(db: AsyncSession, lot_id: int):
        """Get all bids for a specific lot"""
        result = await db.execute(
            select(Bid)
            .where(Bid.lot_id == lot_id)
            .order_by(Bid.created_at.desc())
        )
        return result.scalars().all()