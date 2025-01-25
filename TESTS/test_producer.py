# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev


import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch
from Producer.producer import TimestampProducer

# Constants
REDIS_MODULE = 'redis.Redis'
TIMESTAMP_KEY = 'current_timestamp'


def test_publish_timestamp():
    """
    Test the publish_timestamp method of TimestampProducer

    This test verifies two key behaviors:
    1. The method calls Redis 'set' method exactly once
    2. The timestamp being set is a valid numeric string
    """
    # Use patch to mock Redis connection and prevent actual Redis calls
    with patch(REDIS_MODULE) as mock_redis:
        # Create a TimestampProducer instance
        producer = TimestampProducer()

        # Call the method being tested
        producer.publish_timestamp()

        # Assert that Redis 'set' method was called exactly once
        mock_redis.return_value.set.assert_called_once()

        # Extract the arguments passed to Redis 'set' method
        key, val = mock_redis.return_value.set.call_args[0]

        # Verify the key is correct
        assert key == TIMESTAMP_KEY

        # Verify the value is a numeric string (valid timestamp)
        assert val.isdigit()
