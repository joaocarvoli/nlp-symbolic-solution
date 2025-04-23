import os
import pandas as pd
from helpers.read_dict import read_dic_file

class DictionaryLoader:

    def load(self, file_path: str = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        if file_path is None:
            try:
                src_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                symbolic_base_dir_path = os.path.dirname(src_dir_path)
                project_symbolic_dir_path = os.path.dirname(symbolic_base_dir_path)

                default_path = os.path.join(project_symbolic_dir_path, 'data', 'LIWC2015_pt2-sem-pulo-linhas.dic')

            except NameError:
                 base_path = os.getcwd()
                 default_path = os.path.join(base_path, 'symbolic', 'data', 'LIWC2015_pt2-sem-pulo-linhas.dic')
                 print(default_path)

            file_path = default_path
            print(f"Using default dictionary path: {file_path}") # Debug print


        try:
            categories, entries = read_dic_file(file_path)
            print(f"Successfully read dictionary file from: {file_path}") # Success message
        except FileNotFoundError:
            print(f"Error: Dictionary file not found at {file_path}")
            # Return empty DataFrames on error
            return pd.DataFrame(columns=['category_id', 'category_name']), \
                   pd.DataFrame(columns=['word', 'is_wildcard', 'category_ids'])
        except Exception as e:
            print(f"Error reading dictionary file: {e}")
            # Return empty DataFrames on error
            return pd.DataFrame(columns=['category_id', 'category_name']), \
                   pd.DataFrame(columns=['word', 'is_wildcard', 'category_ids'])

        # Create DataFrames only if loading was successful
        categories_df = pd.DataFrame([
            {"category_id": cat.id, "category_name": cat.name}
            for cat in categories.values()
        ])

        entries_df = pd.DataFrame([
            {
                "word": entry.word,
                "is_wildcard": entry.is_wildcard,
                "category_ids": entry.category_ids
            }
            for entry in entries
        ])

        print(f"Loaded {len(categories_df)} categories and {len(entries_df)} entries.")
        return categories_df, entries_df