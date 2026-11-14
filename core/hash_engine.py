import hashlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Dict, List

def compute_file_hash(file_path: str, chunk_size: int = 65536) -> str:
    """Oblicza skrót SHA-256 dla pojedynczego pliku"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return ""

class HashEngine:
    """Klasa zarządzająca obliczaniem skrótów plików"""

    @staticmethod
    def compute_threaded(file_paths: List[str], max_workers: int = 4) -> Dict[str, str]:

        """Przetwarzanie współbieżne z użyciem wątków"""
        results: Dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {executor.submit(compute_file_hash, path): path for path in file_paths}
            for future in future_to_path:
                path = future_to_path[future]
                results[path] = future.result()
        return results

    @staticmethod
    def compute_multiprocess(file_path: List[str], max_workers: int = 4) -> Dict[str, str]:
        """Przetwarzanie równoległe z użyciem procesów"""
        results: Dict[str, str] = {}
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_path = {executor.submit(compute_file_hash, path):path for path in file_path}
            for future in future_to_path:
                path = future_to_path[future]
                result[path] = future.results()
            return results
