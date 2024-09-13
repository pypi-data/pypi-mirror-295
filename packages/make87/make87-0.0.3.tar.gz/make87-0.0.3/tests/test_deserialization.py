import pytest
from pydantic import ValidationError
from typing import List
from make87 import PUB, SUB, Sockets  # Replace 'your_module' with the actual module name


def test_pub_serialization():
    pub_instance = PUB(socket_type="PUB", topic_name="topic1", address="127.0.0.1", port=8080)
    serialized = pub_instance.json()
    deserialized = PUB.model_validate_json(serialized)

    assert deserialized.socket_type == pub_instance.socket_type
    assert deserialized.topic_name == pub_instance.topic_name


def test_sub_serialization():
    sub_instance = SUB(socket_type="SUB", topic_name="topic2")
    serialized = sub_instance.json()
    deserialized = SUB.model_validate_json(serialized)

    assert deserialized.socket_type == sub_instance.socket_type
    assert deserialized.topic_name == sub_instance.topic_name


def test_sockets_serialization():
    pub_instance = PUB(socket_type="PUB", topic_name="topic1")
    sub_instance = SUB(socket_type="SUB", topic_name="topic2")

    sockets_instance = Sockets(sockets=[pub_instance, sub_instance])
    serialized = sockets_instance.json()
    deserialized = Sockets.model_validate_json(serialized)

    assert len(deserialized.sockets) == 2
    assert isinstance(deserialized.sockets[0], PUB)
    assert not isinstance(deserialized.sockets[0], SUB)
    assert isinstance(deserialized.sockets[1], SUB)
    assert not isinstance(deserialized.sockets[1], PUB)
    assert deserialized.sockets[0].socket_type == "PUB"
    assert deserialized.sockets[1].socket_type == "SUB"


def test_invalid_pub_serialization():
    with pytest.raises(ValidationError):
        PUB(socket_type="PUB", topic_name=2)


def test_invalid_sub_serialization():
    with pytest.raises(ValidationError):
        SUB(socket_type="SUB")


def test_invalid_sockets_serialization():
    pub_instance = PUB(socket_type="PUB", topic_name="topic1")
    invalid_sub_instance = {"socket_type": "SUB"}  # Missing required fields

    with pytest.raises(ValidationError):
        Sockets(sockets=[pub_instance, invalid_sub_instance])


def test_pub_deserialization():
    json_data = '{"socket_type": "PUB", "topic_name": "topic1"}'
    deserialized = PUB.model_validate_json(json_data)

    assert deserialized.socket_type == "PUB"
    assert deserialized.topic_name == "topic1"


def test_sub_deserialization():
    json_data = '{"socket_type": "SUB", "topic_name": "topic2"}'
    deserialized = SUB.model_validate_json(json_data)

    assert deserialized.socket_type == "SUB"
    assert deserialized.topic_name == "topic2"


def test_sockets_deserialization():
    json_data = """
    {
        "sockets": [
            {"socket_type": "PUB", "topic_name": "topic1"},
            {"socket_type": "SUB", "topic_name": "topic2"}
        ]
    }
    """
    deserialized = Sockets.model_validate_json(json_data)

    assert len(deserialized.sockets) == 2
    assert isinstance(deserialized.sockets[0], PUB)
    assert not isinstance(deserialized.sockets[0], SUB)
    assert isinstance(deserialized.sockets[1], SUB)
    assert not isinstance(deserialized.sockets[1], PUB)
    assert deserialized.sockets[0].socket_type == "PUB"
    assert deserialized.sockets[1].socket_type == "SUB"


def test_invalid_pub_deserialization():
    json_data = '{"socket_type": "PUB", "topic_name": 2}'
    with pytest.raises(ValidationError):
        PUB.model_validate_json(json_data)


def test_invalid_sub_deserialization():
    json_data = '{"socket_type": "SUB"}'  # Missing required field 'topic_name'
    with pytest.raises(ValidationError):
        SUB.model_validate_json(json_data)


def test_invalid_sockets_deserialization():
    json_data = """
    {
        "sockets": [
            {"socket_type": "PUB", "topic_name": "topic1", "address": "127.0.0.1", "port": 8080},
            {"socket_type": "SUB"}  # Missing required field 'topic_name'
        ]
    }
    """
    with pytest.raises(ValidationError):
        Sockets.model_validate_json(json_data)
