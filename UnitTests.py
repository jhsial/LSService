import unittest
from starlette.testclient import TestClient
from LSService import app


class TestDirectoryList(unittest.IsolatedAsyncioTestCase):

    async def test_directory_list_valid_path(self):
        # Create a TestClient for the Starlette app
        client = TestClient(app)

        # Send a POST request with valid JSON data asynchronously
        response = client.post(
            '/dir/list',
            json={'path': '/tmp', 'response_delay': 0}
        )

        # Check if the response is a JSONResponse with a 200 status code
        self.assertEqual(200, response.status_code)

        # Check if the response contains a list of files
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertTrue(len(response_data) > 0)

    async def test_directory_list_invalid_path(self):
        # Create a TestClient for the Starlette app
        client = TestClient(app)

        # Send a POST request with invalid JSON data (missing 'path' parameter) asynchronously
        response = client.post(
            '/dir/list',
            json={'response_delay': 0}
        )

        # Check if the response is 400
        self.assertEqual(400, response.status_code)

        # Check if the response contains an error message
        response_data = response.json()
        self.assertEqual(response_data, {"error": "Missing request parameter: path"})


if __name__ == '__main__':
    unittest.main()
