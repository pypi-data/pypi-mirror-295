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
        use_opinionated_stream_handler: bool = False,
    ):
        self.endpoint = endpoint
        self.namespace = "default" if namespace is None else namespace
        self.topic = "default" if topic is None else topic
        self.handler = Handler(self.endpoint, self.namespace, self.topic)
        super().__init__(name, logging.DEBUG)
        super().addHandler(self.handler)
        self.additional_handlers = []
        if use_opinionated_stream_handler:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(PrettyFormatter())
            self.additional_handlers.append(stream_handler)
            super().addHandler(stream_handler)

    def addHandler(self, handler: logging.Handler):
        self.additional_handlers.append(handler)
        super().addHandler(handler)

    def getChild(self, suffix: str) -> "Logger":
        child = Logger(
            self.name + "_" + suffix, self.endpoint, self.namespace, self.topic
        )
        for handler in self.additional_handlers:
            child.addHandler(handler)
        child.additional_handlers = self.additional_handlers
        return child


class PrettyFormatter(logging.Formatter):

    def __init__(self, style_level: bool = True, style_message: bool = True):
        super().__init__()

        yellow = "\033[33;20m"
        blue = "\033[0;34m"
        red = "\033[0;31m"
        bold_red = "\033[1;31m"
        reset = "\033[0m"

        debug = "[ DBUG ]"
        info = "[ INFO ]"
        error = "[ ERRO ]"
        warning = "[ WARN ]"
        critical = "[ CRIT ]"

        style_debug = ""
        style_info = blue
        style_warning = yellow
        style_error = red
        style_critical = bold_red

        message = " [%(name)s] %(message)s"

        if style_level and style_message:
            fmt_debug = style_debug + debug + message + reset
            fmt_info = style_info + info + message + reset
            fmt_warning = style_warning + warning + message + reset
            fmt_error = style_error + error + message + reset
            fmt_critical = style_critical + critical + message + reset

        elif style_level and not style_message:
            fmt_debug = style_debug + debug + reset + message
            fmt_info = style_info + info + reset + message
            fmt_warning = style_warning + warning + reset + message
            fmt_error = style_error + error + reset + message
            fmt_critical = style_critical + critical + reset + message

        elif not style_level and style_message:
            fmt_debug = debug + style_debug + message + reset
            fmt_info = info + style_info + message + reset
            fmt_warning = warning + style_warning + message + reset
            fmt_error = error + style_error + message + reset
            fmt_critical = critical + style_critical + message + reset

        else:
            fmt_debug = debug + message
            fmt_info = info + message
            fmt_warning = warning + message
            fmt_error = error + message
            fmt_critical = critical + message

        self.FORMATTERS = {
            logging.DEBUG: logging.Formatter(fmt=fmt_debug),
            logging.INFO: logging.Formatter(fmt=fmt_info),
            logging.WARNING: logging.Formatter(fmt=fmt_warning),
            logging.ERROR: logging.Formatter(fmt=fmt_error),
            logging.CRITICAL: logging.Formatter(fmt=fmt_critical),
        }

    def format(self, record):
        log_fmt = self.FORMATTERS.get(record.levelno)
        formatter = log_fmt if log_fmt else self.FORMATTERS[logging.INFO]
        return formatter.format(record)
