import logging
import time
import unittest

from cobra.utils.urls import BASE_URL
from cobra.utils.requests import session


class TestUtils(unittest.TestCase):
    """Test utils."""
    def test_API_available(self):
        """Test if API is available."""
        logging.info(f"Testing if API is available at {BASE_URL}.")
        r = session.get(BASE_URL)
        self.assertEqual(r.status_code, 200)

    def test_rate_limit(self, per_second=5):
        """Check that limited to 5 per second (default)."""
        with session.cache_disabled():  # Otherwise cache will hide rate limiting
            time.sleep(10)  # Wait for local and server rate limit to reset
            t0 = time.time()
            # Make sure over burst
            print("Saturate")
            for i in range(per_second * 2):
                r = session.get(BASE_URL)
                print(f"{time.time() - t0:.2f}")
            # Measure time during limiting
            print("Limiting")
            t2 = time.time()
            for i in range(per_second * 2):
                r = session.get(BASE_URL)
                self.assertEqual(r.status_code, 200)
                print(f"{time.time() - t0:.2f}")
            t3 = time.time()
            self.assertGreater(t3 - t2, 1.5)  # Need significantly more than a single cycle
