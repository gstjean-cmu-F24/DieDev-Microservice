# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev


import os
import sys
from unittest.mock import patch

from Producer.producer import TimestampProducer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constants
REDIS_MODULE = 'redis.Redis'
TIMESTAMP_KEY = 'current_timestamp'

def test_publish_timestamp():
    with patch(REDIS_MODULE) as mock_redis:
        producer = TimestampProducer()
        producer.publish_timestamp()
        mock_redis.return_value.set.assert_called_once()
        key, val = mock_redis.return_value.set.call_args[0]
        assert key == TIMESTAMP_KEY
        assert val.isdigit()


