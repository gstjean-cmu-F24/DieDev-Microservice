import time
import redis
import schedule
import os
from datetime import datetime

class TimestampProducer:
    def __init__(self, redis_host=None, redis_port=6379):
        redis_host = redis_host or os.getenv('REDIS_HOST', 'redis')
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
    
    def publish_timestamp(self):
        current_timestamp = int(time.time())
        self.redis_client.set('current_timestamp', str(current_timestamp))
        print(f"Published timestamp: {current_timestamp}")

def run_producer():
    producer = TimestampProducer()
    producer.publish_timestamp()  # Publish immediately on startup
    schedule.every(5).seconds.do(producer.publish_timestamp)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_producer()