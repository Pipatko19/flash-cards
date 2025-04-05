import json
import uuid

FILENAME = 'flashcards.json'

def save_to_file(filename, **items):
    """Saves flashcards to a JSON file."""
    print(items)
    if 'id' not in items:
        items['id'] = str(uuid.uuid4())
    body = {'sets': [items]}
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(body, file, indent=2, ensure_ascii=False)

def load_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['sets'][0]

def load_sets(filename):
    """Load names from a JSON file"""
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    sets = []
    for set in data['sets']:
        count = str(len(set['flashcards']))
        sets.append((set['title'], count, set['description'], set['tags']))
    return sets

if __name__ == '__main__':
    print(load_sets('flashcards.json'))