"""Тесты для модуля processing_json"""

import io
import sys
import unittest
from unittest.mock import MagicMock, patch

from json_processing import process_json


class TestProcessJson(unittest.TestCase):
    """Тесты для функции process_json."""

    def test_basic_functionality(self):
        """Тест поиск токенов в JSON"""
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1"]
        tokens = ["WORD1", "word2"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)

        # Проверяем что callback вызвался с правильными параметрами
        expected_calls = [
            unittest.mock.call("key1", "WORD1"),
            unittest.mock.call("key1", "word2"),
        ]
        mock_callback.assert_has_calls(expected_calls, any_order=True)

    def test_case_insensitive_token_matching(self):
        """Тест регистронезависимого поиска токенов"""
        json_str = '{"key1": "Word1 WORD1 wOrD1"}'
        required_keys = ["key1"]
        tokens = ["word1"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)

        self.assertEqual(mock_callback.call_count, 3)
        mock_callback.assert_called_with("key1", "word1")

    def test_case_sensitive_key_matching(self):
        """Тест что ключи ищутся с учетом регистра"""
        json_str = '{"Key1": "word1", "key1": "word2"}'
        required_keys = ["Key1"]
        tokens = ["word1", "word2"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        mock_callback.assert_called_once_with("Key1", "word1")

    def test_multiple_keys_processing(self):
        """Тест обработки нескольких ключей"""
        json_str = '{"key1": "token1", "key2": "token2", "key3": "token3"}'
        required_keys = ["key1", "key2"]
        tokens = ["token1", "token2", "token3"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)

        expected_calls = [
            unittest.mock.call("key1", "token1"),
            unittest.mock.call("key2", "token2"),
        ]
        mock_callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_callback.call_count, 2)

    def test_key_not_found_in_json(self):
        """Тест когда ключ из required_keys отсутствует в JSON"""
        json_str = '{"key1": "token1"}'
        required_keys = ["key1", "missing_key"]
        tokens = ["token1"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        mock_callback.assert_called_once_with("key1", "token1")

    def test_empty_json(self):
        """Тест с пустым JSON"""
        json_str = "{}"
        required_keys = ["key1"]
        tokens = ["token1"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        mock_callback.assert_not_called()

    def test_none_parameters(self):
        """Тест когда переданы None параметры"""
        json_str = '{"key1": "token1"}'
        mock_callback = MagicMock()

        process_json(json_str, None, ["token1"], mock_callback)
        mock_callback.assert_not_called()

        process_json(json_str, ["key1"], None, mock_callback)
        mock_callback.assert_not_called()

        process_json(json_str, ["key1"], ["token1"], None)

    def test_empty_lists(self):
        """Тест с пустыми списками required_keys или tokens"""
        json_str = '{"key1": "token1"}'
        mock_callback = MagicMock()

        process_json(json_str, [], ["token1"], mock_callback)
        mock_callback.assert_not_called()

        process_json(json_str, ["key1"], [], mock_callback)
        mock_callback.assert_not_called()

    def test_token_not_found_in_value(self):
        """Тест когда токены не найдены в значении"""
        json_str = '{"key1": "value1 value2"}'
        required_keys = ["key1"]
        tokens = ["token1", "token2"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_multiple_spaces_handling(self):
        """Тест обработки множественных пробелов"""
        json_str = '{"key1": "  word1   word2  word3  "}'
        required_keys = ["key1"]
        tokens = ["word1", "word2", "word3"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        self.assertEqual(mock_callback.call_count, 3)

    def test_special_characters_in_words(self):
        """Тест что функция работает только с буквами и цифрами"""
        json_str = '{"key1": "word1 word2! word3@ test123"}'
        required_keys = ["key1"]
        tokens = ["word1", "word2", "word3", "test123"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        expected_calls = [
            unittest.mock.call("key1", "word1"),
            unittest.mock.call("key1", "test123"),
        ]
        mock_callback.assert_has_calls(expected_calls, any_order=True)

    def test_duplicate_tokens_in_value(self):
        """Тест когда один токен встречается несколько раз в значении"""
        json_str = '{"key1": "word1 word1 word1"}'
        required_keys = ["key1"]
        tokens = ["word1"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        self.assertEqual(mock_callback.call_count, 3)

    def test_original_token_preservation(self):
        """Тест что callback получает оригинальный токен из tokens"""
        json_str = '{"key1": "Word1"}'
        required_keys = ["key1"]
        tokens = ["WORD1"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        mock_callback.assert_called_with("key1", "WORD1")

    def test_complex_json_structure(self):
        """Тест с более сложной JSON структурой (вложенные объекты игнорируются по условию)"""
        json_str = '{"key1": "token1", "nested": {"inner": "token2"}, "key2": "token3"}'
        required_keys = ["key1", "key2", "nested"]
        tokens = ["token1", "token2", "token3"]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)

        expected_calls = [
            unittest.mock.call("key1", "token1"),
            unittest.mock.call("key2", "token3"),
        ]
        mock_callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_callback.call_count, 2)

    def test_large_input(self):
        """Тест с большим количеством данных"""
        import json

        data = {f"key{i}": f"word{i} " * 10 for i in range(10)}
        json_str = json.dumps(data)
        required_keys = [f"key{i}" for i in range(10)]
        tokens = [f"word{i}" for i in range(10)]

        mock_callback = MagicMock()
        process_json(json_str, required_keys, tokens, mock_callback)
        self.assertEqual(mock_callback.call_count, 100)


if __name__ == "__main__":
    unittest.main()
