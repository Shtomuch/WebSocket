# Auction Service

Real-time auction service built with FastAPI, PostgreSQL, and WebSocket support.

## Features

- Create and manage auction lots
- Place bids via REST API
- Real-time bid updates through WebSocket
- PostgreSQL for data persistence
- Docker containerization

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **PostgreSQL** - Database for storing lots and bids
- **SQLAlchemy** - ORM for database operations
- **WebSocket** - Real-time communication
- **Docker** - Containerization

## Project Structure

```
.
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configuration
│   ├── db/            # Database setup
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── main.py        # Application entry point
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

## Installation & Setup

### Prerequisites

- Docker and Docker Compose installed
- Git

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd WebSocket
```

2. Create `.env` file (already provided with default values):
```env
DATABASE_URL=postgresql+asyncpg://auction_user:auction_pass@db:5432/auction_db
POSTGRES_USER=auction_user
POSTGRES_PASSWORD=auction_pass
POSTGRES_DB=auction_db
```

3. Start the services:
```bash
docker-compose up --build
```

The service will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws/lots/{lot_id}

## API Endpoints

### REST Endpoints

#### Create Lot
```http
POST /lots
Content-Type: application/json

{
  "title": "Vintage Watch",
  "description": "Rare vintage watch from 1960s",
  "start_price": 100.0
}
```

#### Get Active Lots
```http
GET /lots
```

#### Get Specific Lot
```http
GET /lots/{lot_id}
```

#### Place Bid
```http
POST /lots/{lot_id}/bids
Content-Type: application/json

{
  "bidder": "John Doe",
  "amount": 150.0
}
```

#### Get Lot Bids
```http
GET /lots/{lot_id}/bids
```

#### End Lot Auction
```http
POST /lots/{lot_id}/end
```

### WebSocket Endpoint

Connect to receive real-time updates for a specific lot:
```
ws://localhost:8000/ws/lots/{lot_id}
```

Message format for bid updates:
```json
{
  "type": "bid_placed",
  "lot_id": 1,
  "bidder": "John",
  "amount": 105
}
```

## Testing with cURL

### Create a lot:
```bash
curl -X POST "http://localhost:8000/lots" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Lot", "description": "Test description", "start_price": 50.0}'
```

### Place a bid:
```bash
curl -X POST "http://localhost:8000/lots/1/bids" \
  -H "Content-Type: application/json" \
  -d '{"bidder": "Alice", "amount": 75.0}'
```

### Get active lots:
```bash
curl "http://localhost:8000/lots"
```

## WebSocket Testing

You can test WebSocket connection using `wscat`:

```bash
npm install -g wscat
wscat -c ws://localhost:8000/ws/lots/1
```

Or use the Python client example:

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/lots/1"
    async with websockets.connect(uri) as websocket:
        # Receive connection confirmation
        message = await websocket.recv()
        print(f"Connected: {message}")
        
        # Listen for updates
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Update received: {data}")

asyncio.run(test_websocket())
```

## Development

### Running locally without Docker

1. Install PostgreSQL and create database
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
3. Update `.env` with your local database URL
4. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

The application automatically creates tables on startup. For production, consider using Alembic for migrations.

## API Documentation

Once the service is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
