# Wyszukiwarka zduplikowanych plików
## Opis projektu
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
| Metoda przetwarzania | Czas wykonania |
| :--- | ---: |
| Sekwencyjnie | `~0.0044 s` |
| 4 wątki (`ThreadPoolExecutor`) | `~0.0093 s` |
| 4 procesy (`ProcessPoolExecutor`) | `~0.7406 s` |

### Wnioski dotyczące GIL
1. GIL w Pythonie ogranicza współbieżne wykonywanie kodu bajtowego przez wiele wątków w obrębie jednego procesu
2. Dzięki zwolnieniu GIL wątki mogą efektywnie współdzielić czas procesora, co znacząco skraca czas przetwarzania
3. Przy mniejszej liczbie plików narzut związany z inicjalizacją i komunikacją między procesorami może sprawić, że procesy będą działać wolniej niż wątki
4. Operacje systemowe zwalniają blokadę GIL, pozwalając innym wątkom na efektywną pracę w tym samym czasie
5. Wątki doskonale sprawdzają się przy operacjach I/O i hashowaniu blokowym zwalniającym GIL

### Problemy napotkane podczas tworzenia projektu
1. Literówki i błędy w kodzie podczas pisania modułów
2. Brak odpowiedniej funkcji do obsługi rekurencji np. przy pisaniu generatora scan_files() początkowo użyłem yield sub_scanner.scan_files(), przez co zamiast ścieżek do plików zwracane były obiekty generatora. Problem został usunięty po zastosowaniu yield from
3. Brak metody setdefault() przy grupowaniu hashy. Przy pisaniu pętli grupującej duplikaty w main.py przypisanie hash_groups[file_hash].append(path) kończyło się błędem. Dopiero po zmianie metody na hash_groups.setdefault(file_hash, []).append(path) przestał wyskakiwać błąd
