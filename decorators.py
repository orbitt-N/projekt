import functools
import time
from typing import Callable, Any

def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """dekorator funkcji mierzący czas jej wykonania"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"[METRYKA] Funkcja '{func.__name__}' wykonała się w {elapsed:.4f} s")
        return result
    return wrapper

def validate_path_exists(min_size_mb: int = 0) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """dekorator z parametrami"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            print(f"[WALIDACJA] Sprawdzanie ścieżki przed wywołaniem '{func.__name__}' (prog: {min_size_mb} MB)...")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator