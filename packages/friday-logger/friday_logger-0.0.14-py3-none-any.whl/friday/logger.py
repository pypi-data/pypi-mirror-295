import logging
from typing import Optional
import requests
from urllib.parse import urljoin
from friday.types import PutLogsRequest


class Handler(logging.Handler):
    def __init__(self, endpoint: str, namespace: str, topic: str):
        super().__init__(logging.DEBUG)
        self.endpoint = endpoint
        self.namespace = namespace
        self.topic = topic

    def emit(self, record: logging.LogRecord):
        put_endpoint = urljoin(self.endpoint, "logs")
        req_body = PutLogsRequest(
            namespace=self.namespace,
            topic=self.topic,
            data=record.getMessage(),
            level=record.levelname,
        )
        requests.put(put_endpoint, json=dict(req_body))


class Logger(logging.Logger):
    def __init__(
        self,
        name: str,
        endpoint: str,
        namespace: Optional[str] = None,
        topic: Optional[str] = None,
    ):
        self.endpoint = endpoint
        self.namespace = "default" if namespace is None else namespace
        self.topic = "default" if topic is None else topic
        self.handler = Handler(self.endpoint, self.namespace, self.topic)
        super().__init__(name, logging.DEBUG)
        super().addHandler(self.handler)
        self.additional_handlers = []

    def addHandler(self, handler: logging.Handler):
        self.additional_handlers.append(handler)
        super().addHandler(handler)

    def getChild(self, suffix: str) -> "Logger":
        child = Logger(
            self.name + "_" + suffix, self.endpoint, self.namespace, self.topic
        )
        for handler in self.additional_handlers:
            child.addHandler(handler)
        return child
