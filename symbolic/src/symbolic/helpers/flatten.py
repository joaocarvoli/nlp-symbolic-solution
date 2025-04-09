from typing import List, Any

def flatten_extend(matrix: List[List[Any]]) -> List[Any]:
    """
        Flattens a 2D list (matrix) into a 1D list by extending the first list with each row.
    """
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list