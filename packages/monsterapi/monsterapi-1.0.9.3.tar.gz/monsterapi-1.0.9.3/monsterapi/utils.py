import os
import time
import logging
import requests
import random
from uuid import uuid4
from functools import wraps

# Use LOGGING_LEVEL environment variable to set logging level
# Default logging level is INFO
level = os.environ.get('LOGGING_LEVEL', 'INFO')

if level == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG)
elif level == 'INFO':
    logging.basicConfig(level=logging.INFO)
elif level == 'WARNING':
    logging.basicConfig(level=logging.WARNING)
elif level == 'ERROR':
    logging.basicConfig(level=logging.ERROR)
elif level == 'CRITICAL':
    logging.basicConfig(level=logging.CRITICAL)

def retry_on_status(codes={400}, retries=3, delay=5):
    """
    Decorator that retries the function when it raises a requests.HTTPError with certain status codes.

    :param codes: The HTTP status codes to retry on, default is {400}.
    :param retries: The number of retries, default is 3.
    :param delay: The delay between retries in seconds, default is 5.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except requests.HTTPError as e:
                    if e.response.status_code in codes:
                        time.sleep(delay)
                    else:
                        raise e
            raise Exception("Maximum retry attempts reached, request failed.")
        return wrapper
    return decorator


ADJECTIVES = [
    "adorable", "ambitious", "brave", "charming", "eager",
    "faithful", "gracious", "happy", "inventive", "jovial",
    "kind", "loyal", "mysterious", "noble", "optimistic",
    "patient", "quirky", "resilient", "sturdy", "thrifty"
]

NOUNS = [
    "albattani", "archimedes", "bose", "carver", "dijkstra",
    "einstein", "fermat", "galileo", "hawking", "joliot",
    "kepler", "lovelace", "mendel", "newton", "pascal",
    "quarks", "rutherford", "sagan", "tesla", "volta"
]

#misc
def generate_random_name(with_uuid = True):
    # Generate a short segment of a UUID (e.g., first 8 characters)
    if with_uuid:
        short_uuid = str(uuid4())[:10]
        return f"{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}_{short_uuid}"
    else:
        return f"{random.choice(ADJECTIVES)}_{random.choice(NOUNS)}"

