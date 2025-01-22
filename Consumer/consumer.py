from fastapi import FastAPI, HTTPException
import redis
from datetime import datetime
import uvicorn
from pydantic import BaseModel
import os

app = FastAPI(title="Timestamp Consumer Service")

class TimestampResponse(BaseModel):
    epoch: int
    human_readable: str

class TimestampConsumer:
    def __init__(self, redis_host=None, redis_port=6379):
        redis_host = redis_host or os.getenv('REDIS_HOST', 'redis')
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
    
    def get_current_timestamp(self):
        timestamp_str = self.redis_client.get('current_timestamp')
        if not timestamp_str:
            raise HTTPException(status_code=404, detail="Timestamp not available")
        return int(timestamp_str)
    
    def convert_to_human_readable(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

consumer = TimestampConsumer()

@app.get("/time", response_model=TimestampResponse)
async def get_time():
    timestamp = consumer.get_current_timestamp()
    human_readable = consumer.convert_to_human_readable(timestamp)
    return TimestampResponse(epoch=timestamp, human_readable=human_readable)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)