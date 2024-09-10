import requests
import time


def request_with_retry(method: str, url: str, **kwargs):
    i = 1
    while True:
        try:
            return requests.request(method, url, **kwargs)
        except:
            print(f"Request attempt {i} failed, retrying...")
            i += 1
            time.sleep(0.1 * i)
            continue
