from datetime import datetime
from friday.types import (
    Log,
    NamespaceAndTopic,
    Level,
    GetLogsRequest,
    Order,
    LogsResponse,
)
from typing import List, Optional
from urllib.parse import urljoin
import requests


class Aggregator:
    def __init__(self, friday_endpoint: str):
        self.friday_endpoint = friday_endpoint

    # TODO: infer these types from QueryInput
    def query(
        self,
        limit: int = 1,
        offset: int = 0,
        namespace: Optional[str] = None,
        topics: list[str] = [],
        levels: list[Level] = [],
        before: Optional[datetime] = None,
        after: Optional[datetime] = None,
        order: Order = Order.DESC,
    ) -> List[Log]:

        req_body = GetLogsRequest(
            limit=limit,
            offset=offset,
            namespace=namespace,
            topics=topics,
            levels=levels,
            before=before,
            after=after,
            order=order,
        )

        resp = requests.post(urljoin(self.friday_endpoint, "logs"), json=dict(req_body))

        json = resp.json()
        data = LogsResponse(**json)
        parsed_data = [log for log in data.logs]
        return parsed_data
