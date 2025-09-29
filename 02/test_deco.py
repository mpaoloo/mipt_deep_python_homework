"""Тесты для модуля с декоратором retry_deco"""

import io
import sys
import unittest
from unittest.mock import patch

from deco import retry_deco


class TestRetryDeco(unittest.TestCase):
    """Тесты для декоратора retry_deco."""

    def test_successful_function_call_with_args(self):
        """Тест успешного вызова функции без ошибок с позиционными аргументами"""

        @retry_deco(3)
        def add(a, b):
            return a + b

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = add(4, 2)

        output = mock_stdout.getvalue()
        self.assertEqual(result, 6)
        self.assertIn('run "add" with positional args = (4, 2)', output)
        self.assertIn("attempt = 1, result = 6", output)

    def test_function_with_keyword_args(self):
        """Тест функции с keyword аргументами"""

        @retry_deco(3)
        def add(a, b):
            return a + b

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = add(4, b=3)

        output = mock_stdout.getvalue()
        self.assertEqual(result, 7)
        self.assertIn("positional args = (4,)", output)
        self.assertIn("keyword kwargs = {'b': 3}", output)
        self.assertIn("attempt = 1, result = 7", output)

    def test_function_with_expected_exception_no_retry(self):
        """Тест что ожидаемые исключения не ведут к перезапуску"""

        @retry_deco(3, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError("test")
            return isinstance(value, int)

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            try:
                check_int(value=None)
            except ValueError:
                pass

        output = mock_stdout.getvalue()
        self.assertEqual(output.count("attempt = 1"), 1)
        self.assertNotIn("attempt = 2", output)
        self.assertIn("exception = ValueError", output)

    def test_function_with_unexpected_exception_retry(self):
        """Тест что неожиданные исключения вызывают перезапуск"""

        @retry_deco(3)
        def failing_func():
            raise RuntimeError("t")

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            try:
                failing_func()
            except RuntimeError:
                pass

        output = mock_stdout.getvalue()
        self.assertIn("attempt = 1, exception = RuntimeError", output)
        self.assertIn("attempt = 2, exception = RuntimeError", output)
        self.assertIn("attempt = 3, exception = RuntimeError", output)

    def test_function_succeeds(self):
        """Тест что функция в итоге успешно выполняется после нескольких исключений"""
        call_count = 0

        @retry_deco(3)
        def failing():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError("test")
            return "success"

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = failing()

        output = mock_stdout.getvalue()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
        self.assertIn("attempt = 1, exception = RuntimeError", output)
        self.assertIn("attempt = 2, exception = RuntimeError", output)
        self.assertIn("attempt = 3, result = success", output)

    def test_default_parameters(self):
        """Тест работы с параметрами по умолчанию"""

        @retry_deco()
        def simple_func():
            return "ok"

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = simple_func()

        output = mock_stdout.getvalue()
        self.assertEqual(result, "ok")
        self.assertIn("result = ok", output)

    def test_multiple_expected_exceptions(self):
        """Тест с несколькими ожидаемыми исключениями"""

        @retry_deco(3, [ValueError, TypeError])
        def func_with_exceptions(exception_type):
            if exception_type == "value":
                raise ValueError()
            elif exception_type == "type":
                raise TypeError()
            else:
                raise RuntimeError()

        # ValueError - не должно быть перезапуска
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            try:
                func_with_exceptions("value")
            except ValueError:
                pass

        output = mock_stdout.getvalue()
        self.assertEqual(output.count("attempt = 1"), 1)
        self.assertNotIn("attempt = 2", output)

        # RuntimeError - должно быть перезапуск
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            try:
                func_with_exceptions("other")
            except RuntimeError:
                pass

        output = mock_stdout.getvalue()
        self.assertIn("attempt = 3", output)

    def test_no_args_no_kwargs_function(self):
        """Тест функции без аргументов"""

        @retry_deco(2)
        def no_args_func():
            return "no args"

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = no_args_func()

        output = mock_stdout.getvalue()
        self.assertEqual(result, "no args")
        self.assertIn('run "no_args_func" with', output)
        self.assertIn("result = no args", output)

    def test_function_with_complex_arguments(self):
        """Тест функции со сложными аргументами"""

        @retry_deco(2)
        def complex_func(a, b=1, *args, **kwargs):
            return f"{a}_{b}_{args}_{kwargs}"

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            result = complex_func(1, 2, 3, c=4)

        output = mock_stdout.getvalue()
        self.assertIn("positional args = (1, 2, 3)", output)
        self.assertIn("keyword kwargs = {'c': 4}", output)
        self.assertIn("attempt = 1", output)

    def test_edge_case_max_retries_1(self):
        """Тест граничного случая с max_retries=1"""
        call_count = 0

        @retry_deco(1)
        def failing_once():
            nonlocal call_count
            call_count += 1
            raise RuntimeError()

        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            try:
                failing_once()
            except RuntimeError:
                pass

        output = mock_stdout.getvalue()
        self.assertEqual(call_count, 1)
        self.assertIn("attempt = 1", output)
        self.assertNotIn("attempt = 2", output)


if __name__ == "__main__":
    unittest.main()
