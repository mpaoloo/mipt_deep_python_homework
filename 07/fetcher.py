#!/usr/bin/env python3
"""
Асинхронный фетчер URL-ов
"""

import asyncio
import aiohttp
import argparse
import time
from typing import List, Tuple


class URLFetcher:
    """Класс для асинхронной загрузки URL"""
    
    def __init__(self, concurrent_requests: int):
        self.concurrent_requests = concurrent_requests
        self.results = []
    
    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> Tuple[str, str, float]:
        """Асинхронно загружает один URL и возвращает результат"""
        start_time = time.time()
        try:
            async with session.get(url.strip(), timeout=aiohttp.ClientTimeout(total=10)) as response:
                content = await response.text()
                end_time = time.time()
                return url, content[:100] + "..." if len(content) > 100 else content, end_time - start_time
        except Exception as e:
            end_time = time.time()
            return url, f"ERROR: {str(e)}", end_time - start_time
    
    async def fetch_all_urls(self, urls: List[str]) -> List[Tuple[str, str, float]]:
        """Асинхронно загружает все URL с ограничением на одновременные запросы"""
        connector = aiohttp.TCPConnector(limit=self.concurrent_requests)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return results
    
    def run(self, urls: List[str]) -> List[Tuple[str, str, float]]:
        """Запускает процесс загрузки URL-ов"""
        self.results = asyncio.run(self.fetch_all_urls(urls))
        return self.results


def read_urls_from_file(filename: str) -> List[str]:
    """Читает URL-ы из файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return []


def print_results(results: List[Tuple[str, str, float]]):
    """Выводит результаты в консоль"""
    for url, content, duration in results:
        print(f"URL: {url}")
        print(f"Content: {content}")
        print(f"Duration: {duration:.2f} seconds")
        print("-" * 50)


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Асинхронный фетчер URL-ов')
    parser.add_argument('concurrent', type=int, help='Количество одновременных запросов')
    parser.add_argument('file', type=str, help='Файл с URL-ами')
    
    args = parser.parse_args()
    
    urls = read_urls_from_file(args.file)
    if not urls:
        return
    fetcher = URLFetcher(args.concurrent)
    results = fetcher.run(urls)
    
    print_results(results)


if __name__ == "__main__":
    main()