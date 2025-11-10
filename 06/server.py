import socket
import threading
import json
import argparse
from collections import Counter
import re
import requests
from urllib.parse import urlparse


class URLProcessor:
    @staticmethod
    def fetch_url_content(url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except Exception:
            return ""

    @staticmethod
    def get_top_k_words(text, k):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        word_counts = Counter(words)
        return dict(word_counts.most_common(k))


class Worker(threading.Thread):
    def __init__(self, worker_id, task_queue, stats_counter, k):
        super().__init__()
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.stats_counter = stats_counter
        self.k = k
        self.daemon = True

    def run(self):
        while True:
            client_socket, url = self.task_queue.get()
            try:
                content = URLProcessor.fetch_url_content(url)
                top_words = URLProcessor.get_top_k_words(content, self.k)
                
                response_data = json.dumps(top_words)
                client_socket.send(response_data.encode())
                
                with self.stats_counter.lock:
                    self.stats_counter.count += 1
                    print(f"Total URLs processed: {self.stats_counter.count}")
                    
            except Exception as e:
                error_response = json.dumps({"error": str(e)})
                client_socket.send(error_response.encode())
            finally:
                client_socket.close()
            self.task_queue.task_done()


class StatsCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()


class MasterServer:
    def __init__(self, host='localhost', port=8888, num_workers=4, k=5):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.k = k
        self.task_queue = queue.Queue()
        self.stats_counter = StatsCounter()
        self.workers = []

    def start_workers(self):
        for i in range(self.num_workers):
            worker = Worker(i, self.task_queue, self.stats_counter, self.k)
            worker.start()
            self.workers.append(worker)

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode().strip()
            if data:
                self.task_queue.put((client_socket, data))
        except Exception:
            client_socket.close()

    def run(self):
        self.start_workers()
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                self.handle_client(client_socket)
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            server_socket.close()


def main():
    parser = argparse.ArgumentParser(description='URL Processing Server')
    parser.add_argument('-w', '--workers', type=int, default=4, 
                       help='Number of worker threads')
    parser.add_argument('-k', type=int, default=5, 
                       help='Number of top words to return')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('-p', '--port', type=int, default=8888, 
                       help='Server port')
    
    args = parser.parse_args()
    
    server = MasterServer(args.host, args.port, args.workers, args.k)
    server.run()


if __name__ == '__main__':
    import queue
    main()