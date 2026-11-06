from typing import List, Dict

class DuplicateGroupIterator:
    """ Własna klasa implementująca iterator do przechodzenia po grupach zduplikowanych plików """
    def __init__(self, duplicates_dict: Dict[str, List[str]]) -> None:
        self._duplicate_groups: List[List[str]] = [
            paths for paths in duplicates_dict.values() if len(paths) > 1
        ]
        self._index = 0
    def __iter__(self) -> 'DuplicateGroupIterator':
        return self
    def __next__(self) -> List[str]:
        if self._index >= len(self._duplicate_groups):
            raise StopIteration
        group = self._duplicate_groups[self._index]
        self._index += 1
        return group