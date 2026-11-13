import time
from typing import List

from core.hash_engine import compute_file_hash

def run_benchmark(file_paths: List[str]) -> None:
    """pomiar porównawczy czasu przetwarzania"""
    if not file_paths:
        print("[BENCHMARK] Brak plików do testów")
        return

    print("\n ROZPOCZECIE POMIARU (GIL)")

    start = time.perf_counter()
    for path in file_paths:
        compute_file_hash(path)
    seq_time = time.perf_counter() - start
    print(f"Sekwencyjnie: {seq_time:.4f} s")

    from concurrent.futures import ThreadPoolExecutor
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(compute_file_hash, file_paths))
    thread_time = time.perf_counter() - start
    print(f"4 wątki:      {thread_time:.4f}")

    from concurrent.futures import ProcessPoolExecutor
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(compute_file_hash, file_paths))
    proc_time = time.perf_counter() - start
    print(f"4 procesy:    {proc_time:.4f} s")
    print("----------------------\n")