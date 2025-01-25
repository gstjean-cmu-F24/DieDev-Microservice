# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev

import os
import time
import redis
import schedule
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration Constants
# Redis connection parameters from environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
SCHEDULE_INTERVAL = int(os.getenv('SCHEDULE_INTERVAL', 5))
TIMESTAMP_KEY = 'current_timestamp'


class TimestampProducer:
    """
    Manages timestamp generation and publishing to Redis.
    Responsible for periodic timestamp updates.
    """

    def __init__(self, redis_host=None, redis_port=None):
        """
        Initialize Redis client with configuration from environment variables.

        Args:
        - redis_host (str, optional): Redis server hostname
        - redis_port (int, optional): Redis server port
        """
        redis_host = redis_host or REDIS_HOST
        redis_port = redis_port or REDIS_PORT

        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def publish_timestamp(self):
        """
        Publish current timestamp to Redis.

        Actions:
        - Retrieve current Unix timestamp
        - Store timestamp in Redis
        - Print published timestamp to console
        """
        current_timestamp = int(time.time())
        self.redis_client.set(TIMESTAMP_KEY, str(current_timestamp))
        print(f"Published timestamp: {current_timestamp}")


def run_producer():
    """
    Initialize and run timestamp producer.

    Workflow:
    - Create TimestampProducer instance
    - Publish initial timestamp
    - Schedule periodic timestamp publishing
    - Continuously run scheduled tasks
    """
    producer = TimestampProducer()
    producer.publish_timestamp()  # Publish immediately on startup

    # Schedule timestamp publishing based on environment interval
    schedule.every(SCHEDULE_INTERVAL).seconds.do(producer.publish_timestamp)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_producer()