#!/usr/bin/env python3
"""WebSocket test client for auction service"""

import asyncio
import websockets
import json


async def test_websocket():
    lot_id = 1  # Use existing lot
    uri = f"ws://localhost:8000/ws/lots/{lot_id}"
    
    print(f"Connecting to {uri}...")
    
    async with websockets.connect(uri) as websocket:
        # Receive connection confirmation
        message = await websocket.recv()
        data = json.loads(message)
        print(f"Connected: {data}")
        
        print("\nListening for bid updates...")
        print("Place bids via API to see real-time updates")
        print("Example: curl -X POST 'http://localhost:8000/lots/1/bids' -H 'Content-Type: application/json' -d '{\"bidder\": \"Test\", \"amount\": 1100.0}'")
        
        # Listen for updates
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"\n[UPDATE] {data}")
            except websockets.exceptions.ConnectionClosed:
                print("\nConnection closed")
                break
            except KeyboardInterrupt:
                print("\nDisconnecting...")
                break


if __name__ == "__main__":
    asyncio.run(test_websocket())