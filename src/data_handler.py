import json
import sys

def load_json(filepath: str) -> list:
    """Loads JSON data from the specified filepath"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" Error: Data file not found at {filepath}")
        sys.exit(1)

def save_json(data: list, filepath: str): # understand open() syntax.
    """Saves data to a JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)