import os
import unittest

import cobra.user
from cobra.utils.urls import BASE_URL
from cobra.utils.requests import session


class TestUserAPI(unittest.TestCase):
    """Test user API."""
    def test_user_login(self,
                        test_user=os.environ.get("TEST_USER", 'cobra@cps.cit.tum.de'),
                        test_password=os.environ.get("TEST_USER_PASSWORD", '!2345678')):
        """Test user.login API."""
        cobra.user.logout()  # Might have been logged in from previous test
        self.assertIsNone(cobra.user._refresh_token)
        with self.assertRaises(ValueError):
            _ = cobra.user.login('totally-made-up-user@not-an-email.com', 'totally-made-up-password')
        token = cobra.user.login(test_user, test_password)
        self.assertIsNotNone(token)
        r = session.post(BASE_URL + 'token/verify/', data={'token': token})
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(cobra.user._refresh_token)
        token = cobra.user.login('m@tum.de')
        r = session.post(BASE_URL + 'token/verify/', data={'token': token})
        self.assertEqual(r.status_code, 200)
