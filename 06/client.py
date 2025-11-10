import socket
import threading
import argparse
import json


class URLClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port

    def send_url(self, url):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            client_socket.send(url.encode())
            
            response = client_socket.recv(4096).decode()
            client_socket.close()
            
            result = json.loads(response)
            print(f"{url}: {result}")
            return result
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None


class ClientWorker(threading.Thread):
    def __init__(self, worker_id, urls, client):
        super().__init__()
        self.worker_id = worker_id
        self.urls = urls
        self.client = client

    def run(self):
        for url in self.urls:
            self.client.send_url(url.strip())


class ClientManager:
    def __init__(self, num_threads, urls_file, host='localhost', port=8888):
        self.num_threads = num_threads
        self.urls = self.load_urls(urls_file)
        self.client = URLClient(host, port)

    @staticmethod
    def load_urls(urls_file):
        with open(urls_file, 'r') as f:
            return f.readlines()

    def distribute_urls(self):
        chunks = [[] for _ in range(self.num_threads)]
        for i, url in enumerate(self.urls):
            chunks[i % self.num_threads].append(url)
        return chunks

    def run(self):
        url_chunks = self.distribute_urls()
        threads = []
        
        for i, chunk in enumerate(url_chunks):
            if chunk:
                thread = ClientWorker(i, chunk, self.client)
                thread.start()
                threads.append(thread)
        
        for thread in threads:
            thread.join()


def main():
    parser = argparse.ArgumentParser(description='URL Processing Client')
    parser.add_argument('threads', type=int, 
                       help='Number of client threads')
    parser.add_argument('urls_file', help='File containing URLs')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('-p', '--port', type=int, default=8888, 
                       help='Server port')
    
    args = parser.parse_args()
    
    client_manager = ClientManager(args.threads, args.urls_file, 
                                 args.host, args.port)
    client_manager.run()


if __name__ == '__main__':
    main()