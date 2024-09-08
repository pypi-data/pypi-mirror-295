from friday import Logger, Aggregator

ENDPOINT = "http://localhost:5001"
# ENDPOINT = "https://friday-api.guneet-homelab.duckdns.org"
logger = Logger(
    "test-logger",
    ENDPOINT,
    "test",
    "test",
)

logger.debug("This is a debug message")

aggregator = Aggregator(ENDPOINT)

print(aggregator.query(limit=2, namespaces=["test"], topics=["test"]))
