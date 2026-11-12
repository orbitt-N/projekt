import os
import re
from typing import Generator, Pattern


class FileScanner:
    """klasa zarządzająca skanowaniem katalogów"""

    def __init__(self, root_dir: str, file_extension_pattern: str = r".*\.(png|jpg|txt|pdf)$") -> None:
        self._root_dir = root_dir
        self._regex: Pattern[str] = re.compile(r"(?P<filename>.+)\.(?P<ext>[a-zA-Z0-9]+)$", re.IGNORECASE)
        self._extension_filter: Pattern[str] = re.compile(file_extension_pattern, re.IGNORECASE)

    @property
    def root_dir(self) -> str:
        """property zwracająca katalog roboczy"""
        return self._root_dir

    @root_dir.setter
    def root_dir(self, value: str) -> None:
        """setter walidujący czy podana ścieżka istnieje"""
        if not os.path.isdir(value):
            raise ValueError(f"Podana ścieżka '{value}') nie jest poprawnym katalogiem!")
        self._root_dir = value

    def scan_files(self) -> Generator[str, None, None]:
        """generator/funkcja zwracająca ścieżki plików"""
        if not os.path.exists(self._root_dir):
            return

        try:
            with os.scandir(self._root_dir) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        sub_scanner = FileScanner(entry.path)
                        yield from sub_scanner.scan_files()
                    elif entry.is_file(follow_symlinks=False):
                        if self._extension_filter.search(entry.name):
                            yield entry.path
        except PermissionError:
            print(f"Brak dostępu do katalogu: {self._root_dir}")