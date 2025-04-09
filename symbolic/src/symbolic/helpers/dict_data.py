import pandas as pd
from symbolic.helpers.read_dict import read_dic_file

class DictData:
    def __init__(self):
        categories, entries  = read_dic_file("../../../dictionary/LIWC2015_pt2-sem-pulo-linhas.dic")

        self._category_df = pd.DataFrame([
            {"category_id": cat.id, "category_name": cat.name}
            for cat in categories.values()
        ])
        
        self._entry_df = pd.DataFrame([
            {
                "word": entry.word,
                "is_wildcard": entry.is_wildcard,
                "category_ids": entry.category_ids
            }
            for entry in entries
        ])

    def get_category_df(self) -> pd.DataFrame:
        """
        Returns a DataFrame containing the categories.
        """
        if self._category_df is None:
            raise ValueError("The DataFrame has not been loaded.")
        
        return self._category_df
    
    def get_entries_df(self) -> pd.DataFrame:
        """
        Returns a DataFrame containing the categories.
        """
        if self._entry_df is None:
            raise ValueError("The DataFrame has not been loaded.")
        
        return self._entry_df