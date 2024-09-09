import requests


def request_with_retry(method: str, url: str, **kwargs):
    for _ in range(3):
        try:
            return requests.request(method, url, **kwargs)
        except:
            continue
    raise requests.RequestException("Failed to send request after 3 retries")
