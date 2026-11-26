# -*- coding: utf-8 -*-

from typing import Any, Iterator, Optional


class LinkedListItem:
    """Узел связного списка."""

    def __init__(self, data: Any = None) -> None:
        """Инициализация узла."""
        self.data = data
        self._next_item = None
        self._previous_item = None

    @property
    def next_item(self) -> Optional['LinkedListItem']:
        """Следующий узел."""
        return self._next_item

    @next_item.setter
    def next_item(self, value: Optional['LinkedListItem']) -> None:
        """Установка следующего узла (автоматически обновляет связи)."""
        self._next_item = value
        if value is not None:
            value._previous_item = self

    @property
    def previous_item(self) -> Optional['LinkedListItem']:
        """Предыдущий узел."""
        return self._previous_item

    @previous_item.setter
    def previous_item(self, value: Optional['LinkedListItem']) -> None:
        """Установка предыдущего узла (автоматически обновляет связи)."""
        self._previous_item = value
        if value is not None:
            value._next_item = self

    def __repr__(self) -> str:
        """Строковое представление узла."""
        return f"LinkedListItem({self.data})"


class LinkedList:
    """Кольцевой двусвязный список."""

    def __init__(self, first_item: Optional[LinkedListItem] = None) -> None:
        """Инициализация списка."""
        self.first_item = first_item

    @property
    def last(self) -> Optional[LinkedListItem]:
        """Последний узел."""
        if self.first_item is None:
            return None
        return self.first_item.previous_item

    def append_left(self, item: Any) -> None:
        """Добавить элемент в начало."""
        new_item = LinkedListItem(item)
        if self.first_item is None:
            new_item.next_item = new_item
            self.first_item = new_item
        else:
            old_first = self.first_item
            old_last = old_first.previous_item
            old_first.previous_item = new_item
            old_last.next_item = new_item
            self.first_item = new_item

    def append_right(self, item: Any) -> None:
        """Добавить элемент в конец."""
        new_item = LinkedListItem(item)
        if self.first_item is None:
            new_item.next_item = new_item
            self.first_item = new_item
        else:
            old_first = self.first_item
            old_last = old_first.previous_item
            old_first.previous_item = new_item
            old_last.next_item = new_item

    def append(self, item: Any) -> None:
        """Добавить элемент в конец (алиас)."""
        self.append_right(item)

    def remove(self, item: Any) -> None:
        """Удалить элемент по данным. Вызывает ValueError, если нет."""
        if self.first_item is None:
            raise ValueError(f"{item} нет в списке")
        current = self.first_item
        while True:
            if current.data == item:
                break
            current = current.next_item
            if current is self.first_item:
                raise ValueError(f"{item} нет в списке")
        if current.next_item is current:
            self.first_item = None
        else:
            prev = current.previous_item
            nxt = current.next_item
            prev.next_item = nxt
            if current is self.first_item:
                self.first_item = nxt

    def insert(self, previous: Any, item: Any) -> None:
        """Вставить новый элемент после узла с данными previous."""
        if self.first_item is None:
            raise ValueError(f"{previous} нет в списке")
        current = self.first_item
        while True:
            if current.data == previous:
                break
            current = current.next_item
            if current is self.first_item:
                raise ValueError(f"{previous} нет в списке")
        new_item = LinkedListItem(item)
        nxt = current.next_item
        current.next_item = new_item
        nxt.previous_item = new_item

    def __len__(self) -> int:
        """Длина списка."""
        if self.first_item is None:
            return 0
        count = 1
        current = self.first_item.next_item
        while current is not self.first_item:
            count += 1
            current = current.next_item
        return count

    def __iter__(self) -> Iterator[LinkedListItem]:
        """Итератор по узлам списка."""
        if self.first_item is None:
            return
        current = self.first_item
        while True:
            yield current
            current = current.next_item
            if current is self.first_item:
                break

    def __getitem__(self, index: int) -> Any:
        """Получение данных по индексу."""
        length = len(self)
        if index < 0:
            index += length
        if index < 0 or index >= length:
            raise IndexError("index out of range")
        current = self.first_item
        for _ in range(index):
            current = current.next_item
        return current.data

    def __contains__(self, item: Any) -> bool:
        """Проверка наличия данных в списке."""
        if self.first_item is None:
            return False
        current = self.first_item
        while True:
            if current.data == item:
                return True
            current = current.next_item
            if current is self.first_item:
                return False

    def __reversed__(self) -> Iterator[Any]:
        """Обратный итератор по данным."""
        if self.first_item is None:
            return
        last = self.first_item.previous_item
        current = last
        while True:
            yield current.data
            current = current.previous_item
            if current is last:
                break
