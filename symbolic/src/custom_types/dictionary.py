from dataclasses import dataclass
from typing import List

@dataclass
class Category:
    id: int
    name: str

@dataclass
class DictionaryEntry:
    word: str
    category_ids: List[int]
    is_wildcard: bool = False