"""Параметризуемый декоратор для логирования
вызовов и перезапуска функций в случае ошибок"""

from typing import List, Type, Optional


def retry_deco(
    max_tries: int = 1,
    expected_exceptions: Optional[List[Type[Exception]]] = None,
):
    """
    Декоратор для повторного выполнения функций при ошибках.

    Args:
        max_retries: Максимальное количество попыток
        expected_exceptions: Список исключений без перезапуска

    Returns:
        Декорированную функцию
    """

    if expected_exceptions is None:
        expected_exceptions = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            args_str = f"positional args = {args}" if args else ""
            kwargs_str = f"keyword kwargs = {kwargs}" if kwargs else ""

            for attempt in range(1, max_tries + 1):
                try:
                    result = func(*args, **kwargs)
                    print(
                        f"""run "{func.__name__}" with {args_str} {kwargs_str}, 
                            attempt = {attempt}, result = {result}"""
                    )
                    return result
                except Exception as e:
                    if any(
                        isinstance(e, exc_type)
                        for exc_type in expected_exceptions
                    ):
                        print(
                            f"""run "{func.__name__}" with {args_str} {kwargs_str}, 
                                attempt = {attempt}, exception = {type(e).__name__}"""
                        )
                        raise e
                    else:
                        print(
                            f"""run "{func.__name__}" with {args_str} {kwargs_str}, 
                                attempt = {attempt}, exception = {type(e).__name__}"""
                        )
                        if attempt == max_tries:
                            raise e

        return wrapper

    return decorator
