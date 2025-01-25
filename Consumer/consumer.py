# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import redis
from datetime import datetime
import uvicorn
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Configuration Constants
# Redis connection parameters from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Application configuration
LOCAL_PORT = int(os.getenv('LOCAL_PORT', 8000))
SCHEDULE_INTERVAL = int(os.getenv('SCHEDULE_INTERVAL', 5))  # Interval in seconds for publishing timestamp

# Constant values for error handling and key management
TIMESTAMP_KEY = 'current_timestamp'
HTTP_NOT_FOUND = 404
ERROR_TIMESTAMP_NOT_AVAILABLE = "Timestamp not available"

# Initialize FastAPI application
app = FastAPI(
    title="Timestamp Consumer Service",
    description="Microservice for retrieving and managing timestamps",
    version="1.0.0"
)


class TimestampResponse(BaseModel):
    """
    Pydantic model for timestamp response.
    Provides structured data for API endpoint.
    """
    epoch: int  # Unix timestamp in seconds
    human_readable: str  # Formatted timestamp string


class TimestampConsumer:
    """
    Manages timestamp retrieval and conversion operations.
    Interacts with Redis for timestamp storage and retrieval.
    """

    def __init__(self):
        """
        Initialize Redis client with configuration from environment variables.
        Supports flexible configuration through .env file.
        """
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )

    def get_current_timestamp(self):
        """
        Retrieve current timestamp from Redis.

        Raises:
        - HTTPException: If timestamp is not available in Redis

        Returns:
        - int: Unix timestamp in seconds
        """
        timestamp_str = self.redis_client.get(TIMESTAMP_KEY)
        if not timestamp_str:
            raise HTTPException(
                status_code=HTTP_NOT_FOUND,
                detail=ERROR_TIMESTAMP_NOT_AVAILABLE
            )
        return int(timestamp_str)

    def convert_to_human_readable(self, timestamp):
        """
        Convert Unix timestamp to human-readable format.

        Args:
        - timestamp (int): Unix timestamp in seconds

        Returns:
        - str: Formatted timestamp in 'YYYY-MM-DD HH:MM:SS' format
        """
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


# Create consumer instance
consumer = TimestampConsumer()


@app.get("/time", response_model=TimestampResponse)
async def get_time():
    """
    API endpoint to retrieve current timestamp.

    Returns:
    - TimestampResponse: Contains epoch and human-readable timestamp
    """
    timestamp = consumer.get_current_timestamp()
    human_readable = consumer.convert_to_human_readable(timestamp)
    return TimestampResponse(epoch=timestamp, human_readable=human_readable)


# Main execution block
if __name__ == "__main__":
    """
    Run the FastAPI application using Uvicorn when script is executed directly.
    Binds to all network interfaces and uses port from environment configuration.
    """
    uvicorn.run(app, host="0.0.0.0", port=LOCAL_PORT)