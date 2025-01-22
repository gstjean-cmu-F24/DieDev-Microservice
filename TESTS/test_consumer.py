import pytest
from unittest.mock import Mock, patch
from timestamp_consumer.consumer import TimestampConsumer
from fastapi.testclient import TestClient
from timestamp_consumer.consumer import app

client = TestClient(app)

def test_get_time_success():
    with patch('redis.Redis') as mock_redis:
        # Mock Redis get method to return a timestamp
        mock_redis.return_value.get.return_value = "1640995200"
        
        response = client.get("/time")
        assert response.status_code == 200
        data = response.json()
        assert "epoch" in data
        assert "human_readable" in data
        assert data["epoch"] == 1640995200

def test_get_time_no_timestamp():
    with patch('redis.Redis') as mock_redis:
        # Mock Redis get method to return None (no timestamp available)
        mock_redis.return_value.get.return_value = None
        
        response = client.get("/time")
        assert response.status_code == 404