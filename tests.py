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

