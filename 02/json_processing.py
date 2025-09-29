import json
from typing import Callable, List, Optional, Union


def process_json(
    json_str: str,
    required_keys: Optional[List[str]] = None,
    tokens: Optional[List[str]] = None,
    callback: Optional[Callable[[str, str], None]] = None,
) -> None:

    if required_keys is None or tokens is None or callback is None:
        return
    data = json.loads(json_str)

    token_map = {}
    for token in tokens:
        token_map[token.lower()] = token

    for key in required_keys:
        if key in data:
            value = data[key]
            if isinstance(value, str):
                words = value.split()

                for word in words:
                    word_lower = word.lower()
                    if word_lower in token_map:
                        callback(key, token_map[word_lower])


if __name__ == "__main__":
    json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    required_keys = ["key1", "KEY2"]
    tokens = ["WORD1", "word2"]
    process_json(
        json_str,
        required_keys,
        tokens,
        lambda key, token: print(f"key={key}, token={token}"),
    )
