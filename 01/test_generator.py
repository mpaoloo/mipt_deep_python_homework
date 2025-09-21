"""Тесты для модуля generator."""

import unittest
from unittest.mock import mock_open, patch
from generator import filter_file


class TestFilterFile(unittest.TestCase):
    """Тесты для функции filter_file."""

    def test_filter_with_search_words(self):
        """Тест фильтрации по поисковым словам"""
        test_content = """Алиса охотник роет вон да
Ашан Ашан анаш
Огород наш земля
Перед берег
Хорошо жить не запретишь"""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["берег", "ашан"], []))
            expected = ["Ашан Ашан анаш\n", "Перед берег\n"]
            self.assertEqual(result, expected)

    def test_filter_with_stop_words(self):
        """Тест исключения стоп-слов"""
        test_content = """Алиса охотник роет вон да
Ашан Ашан анаш
Огород наш земля
Перед берег"""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["ашан"], ["берег"]))
            expected = ["Ашан Ашан анаш\n"]
            self.assertEqual(result, expected)

    def test_case_insensitive_search(self):
        """Тест регистронезависимого поиска"""
        test_content = """АШАН большой
берег реки
небо голубое"""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["ашан", "Берег"], []))
            expected = ["АШАН большой\n", "берег реки\n"]
            self.assertEqual(result, expected)

    def test_empty_file(self):
        """Тест пустого файла"""
        test_content = ""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test_file.txt", ["слово"], []))
            self.assertEqual(result, [])

    def test_no_matching_lines(self):
        """Тест когда нет подходящих строк"""
        test_content = """Один два три
Четыре пять шесть"""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["ашан"], []))
            self.assertEqual(result, [])

    def test_file_object_input(self):
        """Тест передачи файлового объекта вместо пути"""
        # Файловый объект вместо пути
        test_content = """Ашан магазин
Берег моря"""

        file_obj = mock_open(read_data=test_content)()
        result = list(filter_file(file_obj, ["ашан"], []))
        expected = ["Ашан магазин\n"]
        self.assertEqual(result, expected)

    def test_multiple_search_words_in_line(self):
        """Тест когда в строке несколько искомых слов"""
        test_content = """Ашан у берега реки
Просто текст"""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["ашан", "берег"], []))
            expected = ["Ашан у берега реки\n"]
            self.assertEqual(result, expected)

    def test_stop_word_prevents_yield(self):
        """Тест стоп-слово блокирует вывод строки"""
        test_content = """Ашан у берега
Магазин Ашан
"""

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["ашан"], ["берега"]))
            expected = ["Магазин Ашан\n"]
            self.assertEqual(result, expected)

    def test_empty_lines_skipped(self):
        """Тест пропуска пустых строк"""
        test_content = "\nАшан\n    \nБерег"

        with patch("builtins.open", mock_open(read_data=test_content)):
            result = list(filter_file("test.txt", ["ашан", "берег"], []))
            expected = ["Ашан\n", "Берег"]
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
