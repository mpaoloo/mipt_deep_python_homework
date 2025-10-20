"""Тесты для модуля LRU-кэша."""

import pytest
from lru_cache import LRUCache


def test_basic_operations():
    """Тестирование базовых операций get и set."""
    cache = LRUCache(2)
    cache.set("k1", "val1")
    cache.set("k2", "val2")
    
    # Проверка отсутствующего ключа
    assert cache.get("k3") is None
    # Проверка существующих ключей
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"


def test_lru_eviction():
    """Тестирование вытеснения по алгоритму LRU."""
    cache = LRUCache(2)
    cache.set("k1", "val1")
    cache.set("k2", "val2")
    # Добавляем третий элемент - должен вытеснить k2 (самый старый)
    cache.set("k3", "val3")
    
    # Проверяем, что k3 добавлен, k2 вытеснен, k1 остался
    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


def test_dict_interface():
    """Тестирование интерфейса аналогичного словарю."""
    cache = LRUCache(2)
    # Используем синтаксис словаря
    cache["k1"] = "val1"
    cache["k2"] = "val2"
    
    # Проверяем доступ через синтаксис словаря
    assert cache["k1"] == "val1"
    assert cache["k2"] == "val2"
    assert cache["k3"] is None  # Отсутствующий ключ


def test_update_existing():
    """Тестирование обновления существующего ключа."""
    cache = LRUCache(2)
    cache.set("k1", "val1")
    # Обновляем значение существующего ключа
    cache.set("k1", "new_val")
    
    # Проверяем, что значение обновилось
    assert cache.get("k1") == "new_val"


def test_boundary_conditions():
    """Тестирование граничных условий."""
    cache = LRUCache(1)  # Кэш размером 1
    cache.set("k1", "val1")
    # Добавляем второй элемент - должен вытеснить первый
    cache.set("k2", "val2")
    
    # Проверяем вытеснение
    assert cache.get("k1") is None
    assert cache.get("k2") == "val2"


def test_lru_order_after_access():
    """Тестирование изменения порядка при доступе к элементам."""
    cache = LRUCache(3)
    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")
    
    # Обращаемся к k1 - теперь он должен стать самым новым
    cache.get("k1")
    
    # Добавляем новый элемент - должен вытеснить k2 (самый старый)
    cache.set("k4", "val4")
    
    # Проверяем состояние кэша
    assert cache.get("k2") is None  # Вытеснен
    assert cache.get("k1") == "val1"  # Остался (стал новым после доступа)
    assert cache.get("k3") == "val3"  # Остался
    assert cache.get("k4") == "val4"  # Новый элемент


if __name__ == "__main__":
    pytest.main()