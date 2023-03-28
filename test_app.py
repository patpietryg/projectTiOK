import unittest
from app import get_comments_count
from app import app
from fastapi.testclient import TestClient


class TestGetCommentsCount(unittest.TestCase):
    def test_get_comments_count(self):
        # Test a valid post_id
        self.assertEqual(get_comments_count(1), 5)

        # Test an invalid post_id
        self.assertEqual(get_comments_count(99999), 0)

        # Test with a non-integer post_id
        self.assertEqual(get_comments_count('abc'), 0)


class TestReadRoot(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # assert other properties of the response