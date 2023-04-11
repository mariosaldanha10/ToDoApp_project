import unittest
from app import app


class TestLogin(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_valid_login(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        # Should redirect to logged_in page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], 'http://localhost/logged_in')

    def test_invalid_login(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrong_password'
        })
        # Should render login page with error message
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Wrong password', response.data)

"""
The test output shows two failing tests:

test_invalid_login: This test is failing because the string "Wrong password" was not found in the response data. This indicates that the login form did not display the error message when an incorrect password was entered.

test_valid_login: This test is failing because the response status code is 200 (OK) instead of 302 (Found). This indicates that the login form did not redirect to the correct page after a successful login.

To fix these issues, the login functionality needs to be updated to correctly handle invalid logins and redirect to the correct page after a successful login.
"""