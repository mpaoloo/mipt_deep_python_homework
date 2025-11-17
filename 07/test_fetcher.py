import unittest
import os
from fetcher import URLFetcher, read_urls_from_file

class TestURLFetcherMinimal(unittest.TestCase):
    def test_read_urls_from_file(self):
        with open('test_urls.txt', 'w') as f:
            f.write("http://example.com\nhttp://google.com\n")
        
        urls = read_urls_from_file('test_urls.txt')
        self.assertEqual(len(urls), 2)
        
        if os.path.exists('test_urls.txt'):
            os.remove('test_urls.txt')
    
    def test_read_urls_from_file_not_found(self):
        urls = read_urls_from_file('nonexistent_file.txt')
        self.assertEqual(urls, [])
    
    def test_url_fetcher_initialization(self):
        fetcher = URLFetcher(5)
        self.assertEqual(fetcher.concurrent_requests, 5)

if __name__ == '__main__':
    unittest.main()