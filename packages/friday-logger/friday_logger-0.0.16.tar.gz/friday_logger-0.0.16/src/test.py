from friday import Logger, Aggregator

ENDPOINT = "http://localhost:5000"
# ENDPOINT = "https://friday-api.guneet-homelab.duckdns.org"
logger = Logger(
    "test-logger", ENDPOINT, "test", "test", use_opinionated_stream_handler=True
)

logger.debug("This is a debug message")

aggregator = Aggregator(ENDPOINT)

print(aggregator.query(limit=2, namespace="test", topics=["test"]))
