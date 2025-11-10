import unittest
from unittest.mock import patch, MagicMock
import json
from server import URLProcessor, Worker, StatsCounter
import queue


class TestURLProcessor(unittest.TestCase):
    @patch('server.requests.get')
    def test_fetch_url_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "Hello world hello test"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        content = URLProcessor.fetch_url_content("http://test.com")
        self.assertEqual(content, "Hello world hello test")

    @patch('server.requests.get')
    def test_fetch_url_content_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        
        content = URLProcessor.fetch_url_content("http://test.com")
        self.assertEqual(content, "")

    def test_get_top_k_words(self):
        text = "hello world hello test world test test"
        result = URLProcessor.get_top_k_words(text, 2)
        expected = {"test": 3, "hello": 2}
        self.assertEqual(result, expected)

    def test_get_top_k_words_empty(self):
        text = ""
        result = URLProcessor.get_top_k_words(text, 5)
        self.assertEqual(result, {})


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.task_queue = queue.Queue()
        self.stats_counter = StatsCounter()
        self.k = 3

    @patch('server.URLProcessor.fetch_url_content')
    @patch('server.URLProcessor.get_top_k_words')
    def test_worker_processing(self, mock_get_words, mock_fetch):
        mock_fetch.return_value = "test content"
        mock_get_words.return_value = {"test": 1, "content": 1}
        
        mock_socket = MagicMock()
        
        worker = Worker(1, self.task_queue, self.stats_counter, self.k)
        self.task_queue.put((mock_socket, "http://test.com"))
        
        worker.run_once = True
        worker.run = lambda: worker.process_task() if worker.run_once else None
        worker.process_task = lambda: worker._process_next_task()
        
        worker._process_next_task()
        
        mock_socket.send.assert_called_once()
        sent_data = mock_socket.send.call_args[0][0]
        result = json.loads(sent_data.decode())
        self.assertEqual(result, {"test": 1, "content": 1})


class TestStatsCounter(unittest.TestCase):
    def test_stats_counter(self):
        counter = StatsCounter()
        self.assertEqual(counter.count, 0)
        
        with counter.lock:
            counter.count = 5
        self.assertEqual(counter.count, 5)


if __name__ == '__main__':
    unittest.main()