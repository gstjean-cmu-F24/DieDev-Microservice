# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev

from fastapi import FastAPI, HTTPException
import redis
from datetime import datetime
import uvicorn
from pydantic import BaseModel
import os

app = FastAPI(title="Timestamp Consumer Service")


class TimestampResponse(BaseModel):
    epoch: int  # epoch time
    human_readable: str  # human-readable timestamp


class TimestampConsumer:
    def __init__(self, redis_host=None, redis_port=6379):
        # Initialize Redis client with environment variables or default values
        redis_host = redis_host or os.getenv('REDIS_HOST', 'redis')
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def get_current_timestamp(self):
        """
        Retrieve the current timestamp from Redis.
        - Input: None
        - Output: Integer timestamp from Redis
        - Raises HTTPException if the timestamp is not found
        """
        timestamp_str = self.redis_client.get('current_timestamp')
        if not timestamp_str:
            raise HTTPException(status_code=404, detail="Timestamp not available")
        return int(timestamp_str)

    def convert_to_human_readable(self, timestamp):
        """
        Convert a given epoch timestamp to a human-readable format.
        - Input: Integer timestamp
        - Output: String in 'YYYY-MM-DD HH:MM:SS' format
        """
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


consumer = TimestampConsumer()


@app.get("/time", response_model=TimestampResponse)
async def get_time():
    """
    API endpoint to get the current timestamp.
    - Input: None
    - Output: JSON with epoch and human-readable time
    """
    timestamp = consumer.get_current_timestamp()
    human_readable = consumer.convert_to_human_readable(timestamp)
    return TimestampResponse(epoch=timestamp, human_readable=human_readable)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

