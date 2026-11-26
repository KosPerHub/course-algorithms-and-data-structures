# -*- coding: utf-8 -*-

from typing import Optional

from linked_list import LinkedList
from composition import Composition


class PlayList(LinkedList):
    """Плейлист с текущим треком."""

    def __init__(self) -> None:
        """Инициализация пустого плейлиста."""
        super().__init__()
        self.current_item = None

    def play_all(self, item: Optional[Composition] = None) -> Optional[Composition]:
        """Начать проигрывание с указанного трека (или с начала)."""
        if self.first_item is None:
            self.current_item = None
            return None
        if item is None:
            self.current_item = self.first_item
            return self.current_item.data
        current = self.first_item
        while True:
            if current.data == item:
                self.current_item = current
                return self.current_item.data
            current = current.next_item
            if current is self.first_item:
                self.current_item = self.first_item
                return self.current_item.data

    def next_track(self) -> Optional[Composition]:
        """Переключить на следующий трек."""
        if self.current_item is None:
            return None
        self.current_item = self.current_item.next_item
        return self.current_item.data

    def previous_track(self) -> Optional[Composition]:
        """Переключить на предыдущий трек."""
        if self.current_item is None:
            return None
        self.current_item = self.current_item.previous_item
        return self.current_item.data

    @property
    def current(self) -> Optional[Composition]:
        """Текущий трек."""
        if self.current_item is None:
            return None
        return self.current_item.data