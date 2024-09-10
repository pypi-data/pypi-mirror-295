from typing import TypedDict, List, Optional, Literal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class NamespaceAndTopic(BaseModel):
    namespace: str
    topic: str


class Level(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Order(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class Log(BaseModel):
    id: int
    timestamp: datetime
    namespace: str
    topic: str
    level: Level
    data: str


class LogsResponse(BaseModel):
    logs: list[Log]


class GetLogsRequest(BaseModel):
    limit: int = 1
    offset: int = 0
    namespace: Optional[str] = None
    topics: list[str] = []
    levels: list[Level] = []
    before: Optional[datetime] = None
    after: Optional[datetime] = None
    order: Order = Order.DESC


class PutLogsRequest(BaseModel):
    namespace: str
    topic: str
    level: str
    data: str


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
