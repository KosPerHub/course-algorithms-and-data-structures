# -*- coding: utf-8 -*-

class Composition:
    """Музыкальная композиция."""

    def __init__(self, title: str, artist: str, file_path: str) -> None:
        """Инициализация композиции."""
        
        self.title = title
        self.artist = artist
        self.file_path = file_path

    def __str__(self) -> str:
        """Строковое представление для вывода в интерфейсе."""
        return f"{self.artist} — {self.title}"

    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"Composition({self.title!r})"