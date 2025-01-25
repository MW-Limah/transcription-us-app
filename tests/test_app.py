import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_transcribe_route(self):
        response = self.client.post('/api/audio/transcribe')
        self.assertEqual(response.status_code, 400)
