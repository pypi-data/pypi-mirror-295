import pytest
import os
import json
from unittest.mock import patch
import make87 as m87



@pytest.fixture(autouse=True)
def clear_data_sockets():
    # Ensure that Data.sockets is cleared before each test
    m87.cleanup()


def test_create_topic_env_var_not_set():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="`SOCKETS` environment variable not set"):
            m87.get_topic("some_topic")


def test_create_topic_invalid_json_env_var():
    with patch.dict(os.environ, {"SOCKETS": "not a valid json"}):
        with pytest.raises(ValueError):
            m87.get_topic("some_topic")


def test_create_topic_valid_pub():
    socket_data = {"sockets": [{"socket_type": "PUB", "topic_name": "topic1", "address": "127.0.0.1", "port": 8080}]}
    socket_data_json = json.dumps(socket_data)
    with patch.dict(os.environ, {"SOCKETS": socket_data_json}):
        result = m87.get_topic("topic1")
        assert isinstance(result, m87.PublisherTopic)
        assert result.name == "topic1"


def test_create_topic_valid_sub():
    socket_data = {"sockets": [{"socket_type": "SUB", "topic_name": "topic2", "port": 70}]}
    socket_data_json = json.dumps(socket_data)
    with patch.dict(os.environ, {"SOCKETS": socket_data_json}):
        result = m87.get_topic("topic2")
        assert isinstance(result, m87.SubscriberTopic)
        assert result.name == "topic2"


def test_create_topic_not_found():
    socket_data = {"sockets": [{"socket_type": "PUB", "topic_name": "topic1", "address": "127.0.0.1", "port": 8080}]}
    socket_data_json = json.dumps(socket_data)
    with patch.dict(os.environ, {"SOCKETS": socket_data_json}):
        with pytest.raises(ValueError):
            m87.get_topic("some_topic")


def test_create_topic_invalid_socket_type():
    socket_data = {
        "sockets": [{"socket_type": "INVALID_TYPE", "topic_name": "topic1", "address": "127.0.0.1", "port": 8080}]
    }
    socket_data_json = json.dumps(socket_data)
    with patch.dict(os.environ, {"SOCKETS": socket_data_json}):
        with pytest.raises(ValueError):
            m87.get_topic("topic1")
