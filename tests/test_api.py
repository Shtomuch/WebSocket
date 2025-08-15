import pytest
from httpx import AsyncClient
from app.main import app
import json


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_lot():
    """Test creating a new lot"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        lot_data = {
            "title": "Test Lot",
            "description": "Test description",
            "start_price": 100.0
        }
        response = await client.post("/lots", json=lot_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == lot_data["title"]
        assert data["start_price"] == lot_data["start_price"]
        assert data["current_price"] == lot_data["start_price"]
        assert data["status"] == "running"