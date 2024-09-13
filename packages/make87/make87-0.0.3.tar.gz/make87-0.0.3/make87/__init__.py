import atexit
import importlib
import json
import logging
import os
from collections import deque
from datetime import datetime, timedelta, timezone
from functools import partial
from threading import Lock
from typing import List, Callable, Dict, Tuple
from typing import Literal, Annotated, Type
from typing import Optional
from typing import Union

import zenoh
from google.protobuf.message import Message
from make87_messages.text.LogMessage_pb2 import LogMessage
from pydantic import BaseModel, Field

_SESSION: Optional[zenoh.Session] = None


class PUB(BaseModel):
    socket_type: Literal["PUB"]
    topic_name: str
    topic_key: str
    message_type: str


class SUB(BaseModel):
    socket_type: Literal["SUB"]
    topic_name: str
    topic_key: str
    message_type: str


Socket = Annotated[Union[PUB, SUB], Field(discriminator="socket_type")]


class Sockets(BaseModel):
    sockets: List[Socket]


class Peripheral(BaseModel):
    name: str
    mount: Union[str, int]  # support `int` to pass AVFoundation index used on macOS
    # TODO: Fix up above to match structs in make87 core


class Peripherals(BaseModel):
    peripherals: List[Peripheral]


def _import_class_from_string(path) -> Type[Message]:
    *module_path, class_name = path.split(".")
    # Append `_messages` to package name, so it's `make87_messages`
    module_path[0] += "_messages"
    module_name = ".".join(module_path)
    # append `_pb2` to module and class name because this is how protobuf compiler names them
    module_name += "_pb2"
    # Import the module dynamically
    module = importlib.import_module(module_name)
    # Get the class from the module
    cls = getattr(module, class_name)

    return cls


class MessageMetadata(BaseModel):
    topic_name: str
    topic_key: str


class Topic:
    def __init__(self, name: str):
        self.name = name


class PublisherTopic(Topic):
    def __init__(self, name: str, message_type: str, session: zenoh.Session):
        super().__init__(name)
        # check if session is set otherwise initialize it
        self.name = name
        self._session = session
        self._message_type: Type[Message] = _import_class_from_string(message_type)
        self._pub = session.declare_publisher(f"{name}")

    @property
    def message_type(self) -> Type[Message]:
        return self._message_type

    def publish(self, message: Message) -> None:
        if not message.HasField("timestamp"):
            message.timestamp.FromDatetime(datetime.now(timezone.utc))
        self._pub.put(message.SerializeToString())


class SubscriberTopic(Topic):
    def __init__(self, name: str, message_type: str, session: zenoh.Session):
        super().__init__(name)
        self._subscribers = []
        self.name = name
        self._message_type: Type[Message] = _import_class_from_string(message_type)
        self._session = session

    def decode_message(self, *args, callback: Callable, **kwargs):
        sample = args[0]
        message = self._message_type()
        message.ParseFromString(sample.payload)
        callback(message, MessageMetadata(topic_name=self.name, topic_key=str(sample.key_expr)))

    def subscribe(self, callback: Callable) -> None:
        retrieve_callback = partial(self.decode_message, callback=callback)
        sub = self._session.declare_subscriber(f"{self.name}", retrieve_callback)
        self._subscribers.append(sub)


class MultiSubscriberTopic:
    def __init__(
        self,
        topics: List[SubscriberTopic],
        delta: float = 0.1,
        max_queue_size: int = 10,
    ):
        self._subscriber_topics: List[SubscriberTopic] = topics
        self._buffers: Dict[str, deque] = {topic.name: deque(maxlen=max_queue_size) for topic in topics}
        self._delta: timedelta = timedelta(seconds=delta)
        self._lock: Lock = Lock()  # To ensure thread-safe access to buffers
        self._callback: Optional[Callable] = None  # Store the user-provided callback
        self._max_queue_size: int = max_queue_size  # Maximum size of each queue

    def _buffer_message(self, message: Message, metadata: MessageMetadata):
        """Buffer the incoming message with a timestamp."""
        with self._lock:
            self._buffers[metadata.topic_key].append(
                {"message": message, "metadata": metadata, "timestamp": message.timestamp.ToDatetime()}
            )
            self._try_match_messages()

    def _try_match_messages(self):
        """Attempts to match messages from all topics by continuously comparing the oldest messages."""
        # Step 2: Ensure all queues have at least one message
        while all(len(self._buffers[topic.name]) > 0 for topic in self._subscriber_topics):
            # Step 3: Take the oldest message from each queue
            msg_group = [self._buffers[topic.name][0] for topic in self._subscriber_topics]

            # Get the timestamps of the oldest messages
            timestamps = [msg["timestamp"] for msg in msg_group]

            # Step 4: Check if the messages' timestamps are within the delta
            if max(timestamps) - min(timestamps) <= self._delta:
                # Pass the matched messages to the user's callback
                if self._callback:
                    self._callback(
                        tuple(msg["message"] for msg in msg_group), tuple(msg["metadata"] for msg in msg_group)
                    )

                # Remove the matched messages from the buffers
                for topic in self._subscriber_topics:
                    self._buffers[topic.name].popleft()

                # Exit after successfully matching
                return

            # Step 5: Remove the single oldest message from its queue
            oldest_index = timestamps.index(min(timestamps))
            topic_with_oldest_msg = self._subscriber_topics[oldest_index].name
            self._buffers[topic_with_oldest_msg].popleft()

        # If we exit the while loop, it means one or more buffers are empty, and we cannot proceed further

    def subscribe(self, callback: Callable[[Tuple], None]) -> None:
        """Subscribe to all topics and pass the aggregated messages as a tuple to the provided callback."""
        self._callback = callback  # Store the user-provided callback

        for topic in self._subscriber_topics:
            # Each topic calls _buffer_message as a callback when a message is received
            topic.subscribe(self._buffer_message)


_TOPICS: Dict[str, Union[PublisherTopic, SubscriberTopic]] = {}


def get_topic(name: str) -> Union[PublisherTopic, SubscriberTopic]:
    global _SESSION
    if _SESSION is None:
        initialize()
    global _TOPICS
    if name not in _TOPICS:
        raise ValueError(f"Topic {name} not found. Available topics: {list(_TOPICS.keys())}")

    return _TOPICS[name]


def initialize_peripherals() -> None:
    try:
        peripheral_data_env = os.environ.get("PERIPHERALS", '{"peripherals":[]}')
        peripheral_data = Peripherals.model_validate_json(peripheral_data_env)
    except json.JSONDecodeError:
        raise ValueError("`PERIPHERALS` environment variable is not a valid JSON string.")

    for peripheral in peripheral_data.peripherals:
        peripheral_names.add(peripheral.name, peripheral.mount)


def initialize() -> None:
    try:
        socket_data_env = os.environ["SOCKETS"]
        socket_data = Sockets.model_validate_json(socket_data_env)
    except KeyError:
        raise ValueError("`SOCKETS` environment variable not set")
    except json.JSONDecodeError:
        raise ValueError("`SOCKETS` environment variable is not a valid JSON string.")

    config = None
    if "COMM_CONFIG" in os.environ:
        config = json.loads(os.environ["COMM_CONFIG"])
        config = zenoh.Config.from_obj(config)
    session = zenoh.open(config=config)
    global _TOPICS
    for socket in socket_data.sockets:
        topic_names.add(socket.topic_name, socket.topic_key)
        if isinstance(socket, PUB):
            _TOPICS[socket.topic_key] = PublisherTopic(
                name=socket.topic_key, message_type=socket.message_type, session=session
            )
        elif isinstance(socket, SUB):
            _TOPICS[socket.topic_key] = SubscriberTopic(
                name=socket.topic_key, message_type=socket.message_type, session=session
            )
        else:
            raise ValueError(f"Invalid socket type {socket.socket_type}")

    global _SESSION
    _SESSION = session


def cleanup() -> None:
    global _SESSION
    if _SESSION is not None:
        _SESSION.close()
        _SESSION = None
        global _TOPICS
        _TOPICS = {}


class TopicNamesLookup:
    """Holds topic names and their keys for deployment. Used by developer to put in placeholder in their app logic.
    Is being filled at runtime by the `initialize` function."""

    def __init__(self):
        self._attributes: Optional[Dict[str, str]] = None

    def __getattr__(self, name: str) -> str:
        if self._attributes is None:
            self._attributes = {}
            initialize()
        if name in self._attributes:
            return self._attributes[name]
        else:
            raise AttributeError(
                f"Topic name {name} not found. Make sure it is correctly defined in your `MAKE87` manifest file."
            )

    def add(self, name: str, value: str):
        self._attributes[name] = value


class PeripheralNamesLookup:
    """Holds peripheral names and their mount points for deployment. Used by developer to put in placeholder in their
    app logic. Is being filled at runtime by the `initialize` function."""

    def __init__(self):
        self._attributes: Optional[Dict[str, str]] = None

    def __getattr__(self, name: str) -> str:
        if self._attributes is None:
            self._attributes = {}
            initialize_peripherals()
        if name in self._attributes:
            return self._attributes[name]
        else:
            raise AttributeError(
                f"Peripheral name {name} not found. Make sure it is correctly defined in your `MAKE87` manifest file."
            )

    def add(self, name: str, value: str):
        self._attributes[name] = value


LEVEL_MAPPING = {
    "DEBUG": LogMessage.DEBUG,
    "INFO": LogMessage.INFO,
    "WARNING": LogMessage.WARNING,
    "ERROR": LogMessage.ERROR,
    "CRITICAL": LogMessage.CRITICAL,
}


CWD = os.getcwd()


class ZenohLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self._topic = get_topic(topic_names.LOGS)

    def emit(self, record):

        # Access log information (time, level, message)
        log_msg = LogMessage()
        log_msg.timestamp.FromDatetime(datetime.utcfromtimestamp(record.created))  # Convert and set timestamp
        log_msg.level = LEVEL_MAPPING.get(record.levelname, LogMessage.INFO)  # Map log level
        log_msg.message = record.getMessage()  # Get log message
        log_msg.source = record.name  # Source can be the logger name or module name
        log_msg.file_name = os.path.relpath(
            record.pathname, CWD
        )  # Relative file path (or use record.filename for just the name)
        log_msg.line_number = record.lineno  # Line number

        # Set process and thread IDs as numeric fields
        log_msg.process_id = record.process  # Process ID (integer)
        log_msg.thread_id = record.thread  # Thread ID (integer)

        # Send the structured log entry via Zenoh
        self._topic.publish(message=log_msg)


# Setup logging when the library is imported
def setup_logging():
    # Set up logging to use ZenohLogHandler
    logger = logging.getLogger()
    logger.setLevel(-1)  # Set log level (DEBUG, INFO, etc.)

    # Create a Zenoh log handler
    zenoh_handler = ZenohLogHandler()
    # Add the Zenoh handler to the root logger
    logger.addHandler(zenoh_handler)
    # Register cleanup to run when the script exits
    atexit.register(cleanup_logging)


# Cleanup function to be run on exit
def cleanup_logging():
    for handler in logging.getLogger().handlers:
        handler.flush()
        handler.close()


topic_names = TopicNamesLookup()
peripheral_names = PeripheralNamesLookup()
try:
    setup_logging()
except AttributeError:
    print("No log topic setup. Will not publish logs.")
