"""Модуль реализации LRU-кэша."""

class Node:
    """Узел двусвязного списка для LRU-кэша."""
    
    def __init__(self, key, value):
        """Инициализация узла.
        
        Args:
            key: Ключ для доступа к узлу
            value: Значение, хранимое в узле
        """
        self.key = key
        self.value = value
        self.prev = None  # Ссылка на предыдущий узел
        self.next = None  # Ссылка на следующий узел


class LRUCache:
    """LRU-кэш с фиксированной емкостью.
    
    Attributes:
        limit (int): Максимальное количество элементов в кэше
        cache (dict): Словарь для быстрого доступа к узлам по ключу
        head (Node): Фиктивный узел-голова двусвязного списка
        tail (Node): Фиктивный узел-хвост двусвязного списка
    """
    
    def __init__(self, limit=42):
        """Инициализация LRU-кэша.
        
        Args:
            limit (int): Максимальный размер кэша. По умолчанию 42.
        """
        self.limit = limit
        self.cache = {}
        # Создаем фиктивные узлы головы и хвоста для упрощения логики
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        # Связываем голову и хвост
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Удаляет узел из двусвязного списка.
        
        Args:
            node (Node): Узел для удаления
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        """Добавляет узел в начало списка (после головы).
        
        Args:
            node (Node): Узел для добавления
        """
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Получает значение по ключу из кэша.
        
        При доступе к элемент перемещается в начало как самый новый.
        
        Args:
            key: Ключ для поиска
            
        Returns:
            Значение, связанное с ключом, или None если ключ не найден
        """
        if key in self.cache:
            node = self.cache[key]
            # Перемещаем узел в начало (самый новый)
            self._remove(node)
            self._add_to_head(node)
            return node.value
        return None

    def set(self, key, value):
        """Устанавливает значение по ключу в кэше.
        
        Если ключ уже существует, обновляет значение и делает элемент самым новым.
        Если кэш переполнен, удаляет самый старый элемент.
        
        Args:
            key: Ключ для установки
            value: Значение для установки
        """
        if key in self.cache:
            # Обновление существующего ключа
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_head(node)
        else:
            # Добавление нового ключа
            if len(self.cache) >= self.limit:
                # Удаляем самый старый элемент (перед хвостом)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
            
            # Создаем и добавляем новый узел
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

    def __getitem__(self, key):
        """Получение значения через синтаксис словаря.
        
        Args:
            key: Ключ для поиска
            
        Returns:
            Значение, связанное с ключом, или None если ключ не найден
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """Установка значения через синтаксис словаря.
        
        Args:
            key: Ключ для установки
            value: Значение для установки
        """
        self.set(key, value)