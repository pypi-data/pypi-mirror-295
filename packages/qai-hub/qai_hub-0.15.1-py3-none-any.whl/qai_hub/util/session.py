import backoff
import requests

import qai_hub

# Will sleep {backoff factor} * (2 ** ({number of previous retries})) seconds
BACKOFF_FACTOR = 0.75
# Try 6 times total, for a max total delay of about 20s
MAX_TRIES = 6


def retry_with_backoff():
    """
    Decorator for retrying calls to web services.
    """

    def wrapper(func):
        @backoff.on_exception(
            wait_gen=backoff.expo,
            exception=(
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ),
            max_tries=MAX_TRIES,
        )
        @backoff.on_predicate(
            wait_gen=backoff.expo,
            max_tries=MAX_TRIES,
            predicate=lambda response: response.status_code
            in [
                429,  # Too many requests
                500,  # Internal Server Error
                502,  # Bad Gateway
                503,  # Service Unavailable
                504,  # Gateway Timeout
            ],
        )
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper


class RetryingSessionWithTimeout(requests.Session):
    @retry_with_backoff()
    def request(self, *args, **kwargs):
        # Our webserver is configured to timeout requests after 25 seconds,
        # so we specify a slightly higher max timeout for all requests.
        # By default, requests waits forever.
        # https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts
        default_kwargs = {"timeout": 28}

        return super().request(*args, **{**default_kwargs, **kwargs})


def create_session():
    session = RetryingSessionWithTimeout()
    session.headers.update({"User-Agent": f"qai_hub/{qai_hub.__version__}"})

    return session
