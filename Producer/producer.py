# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev

import time
import redis
import schedule
import os


class TimestampProducer:
    def __init__(self, redis_host=None, redis_port=6379):
        """
        Initialize the TimestampProducer class.

        :param redis_host: Hostname of the Redis server (default is 'redis' from environment variable)
        :param redis_port: Port of the Redis server (default is 6379)
        """
        redis_host = redis_host or os.getenv('REDIS_HOST', 'redis')
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def publish_timestamp(self):
        """
        Publish the current timestamp to the Redis server.

        :return: None
        - Retrieves the current time in seconds since the epoch.
        - Stores the timestamp in Redis with the key 'current_timestamp'.
        - Prints the published timestamp to the console.
        """
        current_timestamp = int(time.time())
        self.redis_client.set('current_timestamp', str(current_timestamp))
        print(f"Published timestamp: {current_timestamp}")


def run_producer():
    """
    Initialize the TimestampProducer and schedule regular timestamp publishing.

    :return: None
    - Instantiates the TimestampProducer.
    - Publishes a timestamp immediately.
    - Schedules the publish_timestamp method to run every 5 seconds.
    - Continuously checks and runs any pending scheduled tasks.
    """
    producer = TimestampProducer()
    producer.publish_timestamp()  # Publish immediately on startup
    schedule.every(5).seconds.do(producer.publish_timestamp)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_producer()
