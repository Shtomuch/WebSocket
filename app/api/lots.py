from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas import LotCreate, LotResponse, BidCreate, BidResponse
from app.services import LotService, BidService
from app.services.websocket_manager import websocket_manager

router = APIRouter(prefix="/lots", tags=["lots"])


@router.post("", response_model=LotResponse, status_code=201)
async def create_lot(
    lot_data: LotCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new auction lot"""
    lot = await LotService.create_lot(db, lot_data)
    return lot


@router.get("", response_model=List[LotResponse])
async def get_active_lots(db: AsyncSession = Depends(get_db)):
    """Get all active auction lots"""
    lots = await LotService.get_active_lots(db)
    return lots


@router.get("/{lot_id}", response_model=LotResponse)
async def get_lot(lot_id: int, db: AsyncSession = Depends(get_db)):
    """Get specific lot by ID"""
    lot = await LotService.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot


@router.post("/{lot_id}/bids", response_model=BidResponse, status_code=201)
async def place_bid(
    lot_id: int,
    bid_data: BidCreate,
    db: AsyncSession = Depends(get_db)
):
    """Place a bid on a lot"""
    try:
        bid = await BidService.place_bid(db, lot_id, bid_data)
        if not bid:
            raise HTTPException(status_code=404, detail="Lot not found or already ended")
        
        # Broadcast bid to WebSocket subscribers
        await websocket_manager.broadcast_bid(lot_id, bid.bidder, bid.amount)
        
        return bid
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{lot_id}/bids", response_model=List[BidResponse])
async def get_lot_bids(lot_id: int, db: AsyncSession = Depends(get_db)):
    """Get all bids for a specific lot"""
    lot = await LotService.get_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    
    bids = await BidService.get_lot_bids(db, lot_id)
    return bids


@router.post("/{lot_id}/end", response_model=LotResponse)
async def end_lot(lot_id: int, db: AsyncSession = Depends(get_db)):
    """End auction for a specific lot"""
    lot = await LotService.end_lot(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found or already ended")
    
    # Broadcast lot ended to WebSocket subscribers
    await websocket_manager.broadcast_lot_ended(lot_id)
    
    return lot