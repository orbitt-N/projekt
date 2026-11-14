from core.scanner import FileScanner
from core.hash_engine import HashEngine
from utils.decorators import measure_time, validate_path_exists
from utils.iterators import DuplicateGroupIterator
from benchmarks.gil_benchmark import run_benchmark


class DuplicateFinderApp:
    """Główna klasa aplikacji zarządzająca procesem wyszukiwania duplikatów."""

    def __init__(self, target_dir: str) -> None:
        self.target_dir = target_dir

    @validate_path_exists(min_size_mb=0)
    @measure_time
    def run(self) -> None:
        print(f"[*] Skanowanie katalogu: {self.target_dir}")

        scanner = FileScanner(self.target_dir)
        file_paths = list(scanner.scan_files())
        print(f"[*] Znaleziono pasujących plików: {len(file_paths)}")

        if not file_paths:
            print("[*] Brak plików do analizy")
            return

        print("[*] Obliczanie skrótów SHA-256")
        file_hashes = HashEngine.compute_threaded(file_paths)

        hash_groups: dict[str, list[str]] = {}
        for path, file_hash in file_hashes.items():
            if not file_hash:
                continue
            hash_groups.setdefault(file_hash, []).append(path)

        duplicate_iterator = DuplicateGroupIterator(hash_groups)

        print("\n WYNIKI: ZNALEZIONE DUPLIKATY")
        found_any = False
        for group in duplicate_iterator:
            found_any = True
            print("\nGrupa duplikatów:")
            for p in group:
                print(f"   - {p}")

        if not found_any:
            print("Nie znaleziono zduplikowanych plików.")

        run_benchmark(file_paths[:30])


if __name__ == "__main__":
    path_to_scan = input("Podaj ścieżkę do przeszukania (np. domyślnie bieżący folder '.'): ").strip()
    if not path_to_scan:
        path_to_scan = "."

    app = DuplicateFinderApp(path_to_scan)
    app.run()