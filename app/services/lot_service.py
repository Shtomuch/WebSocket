from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Lot
from app.models.lot import LotStatus
from app.schemas.lot import LotCreate
from datetime import datetime


class LotService:
    @staticmethod
    async def create_lot(db: AsyncSession, lot_data: LotCreate) -> Lot:
        """Create new auction lot"""
        lot = Lot(
            title=lot_data.title,
            description=lot_data.description,
            start_price=lot_data.start_price,
            current_price=lot_data.start_price,
            status=LotStatus.RUNNING
        )
        db.add(lot)
        await db.commit()
        await db.refresh(lot)
        return lot
    
    @staticmethod
    async def get_lot(db: AsyncSession, lot_id: int) -> Optional[Lot]:
        """Get lot by ID"""
        result = await db.execute(
            select(Lot).where(Lot.id == lot_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_active_lots(db: AsyncSession) -> List[Lot]:
        """Get all active (running) lots"""
        result = await db.execute(
            select(Lot).where(Lot.status == LotStatus.RUNNING)
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_lot_price(db: AsyncSession, lot_id: int, new_price: float) -> Optional[Lot]:
        """Update current price of lot"""
        lot = await LotService.get_lot(db, lot_id)
        if lot:
            lot.current_price = new_price
            await db.commit()
            await db.refresh(lot)
        return lot
    
    @staticmethod
    async def end_lot(db: AsyncSession, lot_id: int) -> Optional[Lot]:
        """End auction for lot"""
        lot = await LotService.get_lot(db, lot_id)
        if lot and lot.status == LotStatus.RUNNING:
            lot.status = LotStatus.ENDED
            lot.ended_at = datetime.utcnow()
            await db.commit()
            await db.refresh(lot)
        return lot