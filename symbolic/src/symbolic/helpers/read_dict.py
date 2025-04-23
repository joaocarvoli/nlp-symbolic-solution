import re
from typing import Tuple, List, Dict

from custom_types.dictionary import Category, DictionaryEntry


def read_dic_file(filepath: str) -> Tuple[Dict[int, Category], List[DictionaryEntry]]:
    categories: Dict[int, Category] = {}
    entries: List[DictionaryEntry] = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_categories = False
    in_words = False

    for line in lines:
        line = line.strip()

        if not line or line.startswith('%'):
            if not in_categories:
                in_categories = True
                continue
            elif in_categories and not in_words:
                in_words = True
                continue
            else:
                continue

        if in_categories and not in_words:
            match = re.match(r'(\d+)\s+([^\t(]+)', line)
            if match:
                cat_id = int(match.group(1))
                cat_name = match.group(2).strip()
                categories[cat_id] = Category(id=cat_id, name=cat_name)

        elif in_words:
            parts = line.split()
            if len(parts) < 2:
                continue
            word = parts[0]
            is_wildcard = word.endswith('*')
            word_clean = word.rstrip('*')

            category_ids = [int(p) for p in parts[1:] if p.isdigit()]
            entry = DictionaryEntry(
                word=word_clean,
                category_ids=category_ids,
                is_wildcard=is_wildcard
            )
            entries.append(entry)

    return categories, entries