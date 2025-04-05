import json

def save_to_file(filename, **items):
    """Saves flashcards to a JSON file."""
    print(items)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(items, file, indent=4, ensure_ascii=False)

def load_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data