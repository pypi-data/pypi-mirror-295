from requests import Session
from requests.adapters import HTTPAdapter
from requests_ratelimiter import LimiterMixin
from requests_cache import CacheMixin
from urllib3 import Retry

from cobra.utils.caches import MAIN_CACHE_DIR


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """Session class with caching and rate-limiting behavior.

    Accepts keyword arguments for both LimiterSession and CachedSession.
    """


"""
Main session object to use when interacting with any part of the CoBRA API.

Features:
 - Rate limiting: <= 5 per second and <= 100 per minute
"""
session = CachedLimiterSession(str(MAIN_CACHE_DIR.joinpath('requests_cache.db')),
                               per_second=5, per_minute=100,
                               expire_after=360, allowable_methods=('GET', 'HEAD'),
                               allowable_codes=(200, ))

retries = Retry(  # Automatically retry on rate limiting
    total=3,
    backoff_factor=.1,
    status_forcelist=[429, ]
)


session.mount('https://', HTTPAdapter(max_retries=retries))
