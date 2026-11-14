# Wyszukiwarka zduplikowanych plików
## Opis projektu i instrukcja uruchamiania
Aplikacja służy do skanowania katalogów, wyszukiwanie zduplikowanych plików na podstawie skrótów kryptograficznych SHA-256 oraz ich grupowania.
Projekt został zrealizowany z wykorzystaniem iteratorów, dekoratorów, generatorów, wyrażeń regularnych oraz współbierzności

### Instrukcja uruchomiania:
1. Otwórz projekt w środowisku programistycznym np. PyCharm.
2. Uruchom główny plik aplikacji "main.py"
3. Po uruchomieniu aplikacji wpisz/wklej ścieżkę katalogu który chcesz zeskanować lub wpisując "." zeskanuje się katalog w którym aktualnie znajduje się aplikacja.

### Tabela mapowania
| Zagadnienie | Gdzie w kodzie |
| :--- | :--- |
| Dekorator funkcji z parametrami | `utils/decorators.py` $\rightarrow$ `validate_path_exists(min_size_mb)` |
| Dekorator metody / property | `core/scanner.py` $\rightarrow$ `FileScanner.root_dir` (`@property` i setter) |
| Iterator | `utils/iterators.py` $\rightarrow$ klasa `DuplicateGroupIterator` |
| Generator | `core/scanner.py` $\rightarrow$ `FileScanner.scan_files()` |
| Wyrażenia regularne (Regex) | `core/scanner.py` $\rightarrow$ `re.compile()` (filtrowanie rozszerzeń i nazewnictwa) |
| Wątki | `core/hash_engine.py` $\rightarrow$ `HashEngine.compute_threaded` (`ThreadPoolExecutor`) |
| Procesy | `core/hash_engine.py` $\rightarrow$ `HashEngine.compute_multiprocess` (`ProcessPoolExecutor`) |
| Pomiar GIL | `benchmarks/gil_benchmark.py` $\rightarrow$ `run_benchmark()` |

### Wyniki pomiarów wydajności
| Metoda przetwarzania | Czas wykonania (30 plików) |
| :--- | ---: |
| Sekwencyjnie | `~0.0450 s` |
| 4 wątki (`ThreadPoolExecutor`) | `~0.0150 s` |
| 4 procesy (`ProcessPoolExecutor`) | `~0.0350 s` |

Wnioski dotyczące GIL
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
