import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import pygame

from linked_list import Composition, PlayList


class PlayerApp:
    """Графический интерфейс плеера."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Простой плеер")
        self.playlist = PlayList()
        self.is_playing = False

        pygame.mixer.init()

        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(padx=10, pady=10)

        frame1 = tk.Frame(root)
        frame1.pack(pady=5)
        tk.Button(frame1, text="Добавить трек",
                  command=self.add_track).pack(side=tk.LEFT, padx=3)
        tk.Button(frame1, text="Удалить трек",
                  command=self.remove_track).pack(side=tk.LEFT, padx=3)
        tk.Button(frame1, text="Выше",
                  command=self.move_up).pack(side=tk.LEFT, padx=3)
        tk.Button(frame1, text="Ниже",
                  command=self.move_down).pack(side=tk.LEFT, padx=3)

        frame2 = tk.Frame(root)
        frame2.pack(pady=5)
        tk.Button(frame2, text="<< Предыдущий",
                  command=self.previous).pack(side=tk.LEFT, padx=3)
        tk.Button(frame2, text="Играть",
                  command=self.play).pack(side=tk.LEFT, padx=3)
        tk.Button(frame2, text="Следующий >>",
                  command=self.next).pack(side=tk.LEFT, padx=3)

        self.status = tk.Label(root, text="Трек не выбран")
        self.status.pack(pady=5)

        self.root.after(1000, self.check_end)

    def update_list(self) -> None:
        """Перерисовать список треков."""
        self.listbox.delete(0, tk.END)
        for item in self.playlist:
            self.listbox.insert(tk.END, str(item.data))

    def add_track(self) -> None:
        """Добавить трек в плейлист."""
        path = filedialog.askopenfilename(
            filetypes=[("Аудио", "*.mp3 *.ogg *.wav")])
        if not path:
            return
        title = simpledialog.askstring(
            "Название", "Название трека:",
            initialvalue=os.path.basename(path))
        if not title:
            return
        comp = Composition(title, "Неизвестен", path)
        self.playlist.append(comp)
        self.update_list()

    def remove_track(self) -> None:
        """Удалить выбранный трек."""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите трек")
            return
        comp = self.playlist[sel[0]]
        if self.playlist.current is comp:
            pygame.mixer.music.stop()
            self.playlist.current_item = None
            self.is_playing = False
        self.playlist.remove(comp)
        self.update_list()

    def move_up(self) -> None:
        """Переместить трек выше."""
        sel = self.listbox.curselection()
        if not sel or sel[0] == 0:
            return
        i = sel[0]
        comp = self.playlist[i]
        is_current = self.playlist.current is comp
        self.playlist.remove(comp)
        if i == 1:
            self.playlist.append_left(comp)
        else:
            prev_prev = self.playlist[i - 2]
            self.playlist.insert(prev_prev, comp)
        if is_current:
            self.playlist.play_all(comp)
        self.update_list()
        self.listbox.selection_set(i - 1)

    def move_down(self) -> None:
        """Переместить трек ниже."""
        sel = self.listbox.curselection()
        if not sel or sel[0] >= len(self.playlist) - 1:
            return
        i = sel[0]
        comp = self.playlist[i]
        is_current = self.playlist.current is comp
        next_comp = self.playlist[i + 1]
        self.playlist.remove(comp)
        self.playlist.insert(next_comp, comp)
        if is_current:
            self.playlist.play_all(comp)
        self.update_list()
        self.listbox.selection_set(i + 1)

    def play(self) -> None:
        """Начать воспроизведение."""
        sel = self.listbox.curselection()
        if sel:
            comp = self.playlist[sel[0]]
            self.playlist.play_all(comp)
        else:
            if self.playlist.current is None:
                self.playlist.play_all()
        self._start_current()

    def next(self) -> None:
        """Следующий трек."""
        if self.playlist.current is None:
            self.play()
            return
        comp = self.playlist.next_track()
        if comp is not None:
            self._start_current()

    def previous(self) -> None:
        """Предыдущий трек."""
        if self.playlist.current is None:
            self.play()
            return
        comp = self.playlist.previous_track()
        if comp is not None:
            self._start_current()

    def _start_current(self) -> None:
        """Воспроизвести текущий трек."""
        comp = self.playlist.current
        if comp is None:
            return
        pygame.mixer.music.load(comp.file_path)
        pygame.mixer.music.play()
        self.is_playing = True
        self.status.config(text=f"Играет: {comp}")

    def check_end(self) -> None:
        """Проверять окончание трека для зацикливания."""
        if self.is_playing and not pygame.mixer.music.get_busy():
            comp = self.playlist.next_track()
            if comp is not None:
                pygame.mixer.music.load(comp.file_path)
                pygame.mixer.music.play()
                self.status.config(text=f"Играет: {comp}")
            else:
                self.is_playing = False
        self.root.after(1000, self.check_end)


def main() -> None:
    """Точка входа."""
    root = tk.Tk()
    PlayerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()