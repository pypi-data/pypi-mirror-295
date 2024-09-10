from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


def find_key(key: str, data: Union[Dict, Sequence], modifier: Optional[Callable[[Any], Any]] = None,
             search_depth: int = 20) -> Tuple[List[Any], List[Any]]:
    """
    Find all appearances of key in a nested dict / sequence combination and return references to each.

    :param key: The key to search for.
    :param data: The data to search in.
    :param modifier: An optional modifier function to apply to each found data.
    :param search_depth: The maximum depth to search in.
    :return: A tuple of lists of all found values with matching key before and after the applied modifier.
    :note: Based on
      https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
    """
    if search_depth < 0:
        raise RecursionError("Maximum search depth exceeded.")
    matched_values = []
    post_modification_values = []
    for k, v in (
            data.items() if isinstance(data, Dict) else enumerate(data) if isinstance(data, Sequence) else []):
        if k == key:
            matched_values.append(data[k])
            if modifier is not None:
                data[k] = modifier(v)
            post_modification_values.append(data[k])
        elif isinstance(v, (Dict, Sequence)) and not isinstance(v, (str, bytes)):
            res = find_key(key, v, modifier, search_depth - 1)
            matched_values += res[0]
            post_modification_values += res[1]
    return matched_values, post_modification_values


def map2path(p: Union[str, Path]) -> Path:
    """Maps strings to paths, but does nothing else s.t., e.g., Django paths are not cast."""
    if isinstance(p, str):
        return Path(p)
    return p
