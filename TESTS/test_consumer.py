# Author: Greenfield Obasi
# Organization: Carnegie Mellon/DieDev


import pytest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Consumer.consumer import TimestampConsumer, TimestampResponse, HTTPException




# Constants for test values
TEST_TIMESTAMP = 1640995200
HUMAN_READABLE_TIMESTAMP = "2022-01-01 02:00:00"
HUMAN_READABLE_RESPONSE = "2022-01-01 00:00:00"
HTTP_NOT_FOUND = 404
TIMESTAMP_KEY = 'current_timestamp'
TIMESTAMP_NOT_AVAILABLE = "Timestamp not available"


def test_get_timestamp_success():
    """
    Test successful timestamp retrieval from Redis.
    Validates that:
    1. get_current_timestamp() returns the correct epoch timestamp
    2. convert_to_human_readable() correctly transforms the timestamp to a human-readable format
    """
    consumer = TimestampConsumer()
    with patch.object(consumer.redis_client, 'get', return_value=str(TEST_TIMESTAMP)):
        timestamp = consumer.get_current_timestamp()
        assert timestamp == TEST_TIMESTAMP
        human_readable = consumer.convert_to_human_readable(timestamp)
        assert human_readable == HUMAN_READABLE_TIMESTAMP


def test_get_timestamp_not_found():
    """
    Test handling of timestamp not found in Redis.
    Validates that:
    1. HTTPException is raised when timestamp is not available
    2. Raised exception has correct status code (404)
    3. Exception detail contains expected error message
    """
    consumer = TimestampConsumer()
    with patch.object(consumer.redis_client, 'get', return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            consumer.get_current_timestamp()
        assert excinfo.value.status_code == HTTP_NOT_FOUND
        assert TIMESTAMP_NOT_AVAILABLE in str(excinfo.value.detail)


def test_timestamp_conversion():
    """
    Test timestamp conversion to human-readable format.
    Validates that convert_to_human_readable() correctly transforms
    an epoch timestamp to its corresponding human-readable representation.
    """
    consumer = TimestampConsumer()
    timestamp = TEST_TIMESTAMP
    human_readable = consumer.convert_to_human_readable(timestamp)
    assert human_readable == HUMAN_READABLE_TIMESTAMP


def test_timestamp_response_model():
    """
    Test the TimestampResponse data model.
    Validates that the model correctly stores:
    1. Epoch timestamp
    2. Human-readable timestamp
    """
    response_data = TimestampResponse(
        epoch=TEST_TIMESTAMP,
        human_readable=HUMAN_READABLE_RESPONSE
    )
    assert response_data.epoch == TEST_TIMESTAMP
    assert response_data.human_readable == HUMAN_READABLE_RESPONSE
