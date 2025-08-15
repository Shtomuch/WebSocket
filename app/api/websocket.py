from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services import LotService
from app.services.websocket_manager import websocket_manager
from app.schemas.websocket import WebSocketMessage, WebSocketMessageType
import logging

router = APIRouter(prefix="/ws", tags=["websocket"])
logger = logging.getLogger(__name__)


@router.websocket("/lots/{lot_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    lot_id: int,
    db: AsyncSession = Depends(get_db)
):
    """WebSocket endpoint for real-time lot updates"""
    # Verify lot exists
    lot = await LotService.get_lot(db, lot_id)
    if not lot:
        await websocket.accept()
        error_message = WebSocketMessage(
            type=WebSocketMessageType.ERROR,
            lot_id=lot_id,
            message="Lot not found"
        )
        await websocket.send_json(error_message.model_dump())
        await websocket.close()
        return
    
    # Connect client
    await websocket_manager.connect(websocket, lot_id)
    
    try:
        # Keep connection alive and handle incoming messages
        while True:
            # Wait for any message from client (ping/pong or other)
            data = await websocket.receive_text()
            # Could handle client messages here if needed
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, lot_id)
        logger.info(f"Client disconnected from lot {lot_id}")
    except Exception as e:
        logger.error(f"WebSocket error for lot {lot_id}: {str(e)}")
        websocket_manager.disconnect(websocket, lot_id)