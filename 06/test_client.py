import unittest
from unittest.mock import patch, MagicMock
import json
from client import URLClient, ClientWorker, ClientManager
import tempfile
import os


class TestURLClient(unittest.TestCase):
    @patch('client.socket.socket')
    def test_send_url_success(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket
        mock_client_socket.recv.return_value = json.dumps(
            {"hello": 2, "world": 1}).encode()
        
        client = URLClient()
        result = client.send_url("http://test.com")
        
        self.assertEqual(result, {"hello": 2, "world": 1})
        mock_client_socket.send.assert_called_once_with(b"http://test.com")
        mock_client_socket.close.assert_called_once()

    @patch('client.socket.socket')
    def test_send_url_failure(self, mock_socket):
        mock_socket.side_effect = Exception("Connection failed")
        
        client = URLClient()
        result = client.send_url("http://test.com")
        
        self.assertIsNone(result)


class TestClientManager(unittest.TestCase):
    def setUp(self):
        self.urls_content = "http://test1.com\nhttp://test2.com\nhttp://test3.com\n"
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write(self.urls_content)
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_load_urls(self):
        manager = ClientManager(2, self.temp_file.name)
        urls = manager.urls
        self.assertEqual(len(urls), 3)
        self.assertEqual(urls[0].strip(), "http://test1.com")

    def test_distribute_urls(self):
        manager = ClientManager(2, self.temp_file.name)
        chunks = manager.distribute_urls()
        self.assertEqual(len(chunks), 2)
        self.assertTrue(len(chunks[0]) + len(chunks[1]) == 3)


class TestClientWorker(unittest.TestCase):
    @patch('client.URLClient')
    def test_client_worker(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        urls = ["http://test1.com", "http://test2.com"]
        worker = ClientWorker(1, urls, mock_client)
        worker.run()
        
        self.assertEqual(mock_client.send_url.call_count, 2)


if __name__ == '__main__':
    unittest.main()