from typing import Dict, Set
from fastapi import WebSocket
import json
from app.schemas.websocket import WebSocketMessage, WebSocketMessageType


class WebSocketManager:
    def __init__(self):
        # Map lot_id to set of active WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, lot_id: int):
        """Accept WebSocket connection and add to lot subscribers"""
        await websocket.accept()
        
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = set()
        
        self.active_connections[lot_id].add(websocket)
        
        # Send connection confirmation
        message = WebSocketMessage(
            type=WebSocketMessageType.CONNECTION_ESTABLISHED,
            lot_id=lot_id,
            message=f"Connected to lot {lot_id} updates"
        )
        await websocket.send_json(message.model_dump())
    
    def disconnect(self, websocket: WebSocket, lot_id: int):
        """Remove WebSocket from lot subscribers"""
        if lot_id in self.active_connections:
            self.active_connections[lot_id].discard(websocket)
            
            # Clean up empty sets
            if not self.active_connections[lot_id]:
                del self.active_connections[lot_id]
    
    async def broadcast_bid(self, lot_id: int, bidder: str, amount: float):
        """Broadcast new bid to all subscribers of a lot"""
        if lot_id not in self.active_connections:
            return
        
        message = WebSocketMessage(
            type=WebSocketMessageType.BID_PLACED,
            lot_id=lot_id,
            bidder=bidder,
            amount=amount
        )
        
        disconnected = set()
        for connection in self.active_connections[lot_id]:
            try:
                await connection.send_json(message.model_dump())
            except:
                # Mark for removal if send fails
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.active_connections[lot_id].discard(conn)
    
    async def broadcast_lot_ended(self, lot_id: int):
        """Broadcast that lot auction has ended"""
        if lot_id not in self.active_connections:
            return
        
        message = WebSocketMessage(
            type=WebSocketMessageType.LOT_ENDED,
            lot_id=lot_id,
            message="Auction has ended for this lot"
        )
        
        for connection in list(self.active_connections[lot_id]):
            try:
                await connection.send_json(message.model_dump())
            except:
                pass
        
        # Clear all connections for ended lot
        if lot_id in self.active_connections:
            del self.active_connections[lot_id]


# Global WebSocket manager instance
websocket_manager = WebSocketManager()