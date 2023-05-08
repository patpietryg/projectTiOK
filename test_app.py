import unittest
from app import get_comments_count
from app import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import xmlrunner


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


class TestGetFavicon(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_favicon(self):
        response = self.client.get("/favicon.ico")
        self.assertEqual(response.status_code, 200)


class TestGetPost(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('requests.get')
    def test_get_posts(self, mock_get):
        post_id = '1'
        post_response_data = {'userId': 1, 'id': 1, 'title': 'test title', 'body': 'test body'}
        user_response_data = {'id': 1, 'name': 'test name', 'username': 'test username'}
        comments_response_data = [
            {'id': 1, 'postId': 1, 'name': 'test name', 'email': 'test@test.com', 'body': 'test comment'}]

        post_response = MagicMock()
        post_response.json.return_value = post_response_data
        user_response = MagicMock()
        user_response.json.return_value = user_response_data
        comments_response = MagicMock()
        comments_response.json.return_value = comments_response_data

        mock_get.side_effect = [post_response, user_response, comments_response]

        response = self.client.get(f"/post/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test title', response.content)
        self.assertIn(b'test body', response.content)
        self.assertIn(b'test name', response.content)
        self.assertIn(b'test comment', response.content)

    def test_get_invalid_post(self):
        # Test retrieving an invalid post
        with TestClient(app) as client:
            response = client.get("/post/invalid_id")
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))