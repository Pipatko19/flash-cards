import json
import uuid

FILENAME = 'flashcards.json'

def save_to_file(filename, **items):
    """Saves flashcards to a JSON file."""
    with open(filename, 'r', encoding='utf-8') as file:    
        data = json.load(file)['sets']

    print(items)
    if items['id'] is None:
        items['id'] = str(uuid.uuid4())
        data.append(items)
        
    else:
        set = get_object_by_id(data, items['id'])
        idx = data.index(set)
        data[idx] = items

    body = {'sets': data}
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(body, file, indent=2, ensure_ascii=False)

def load_from_file(filename, id):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)['sets']
    return get_object_by_id(data, id)


def load_sets(filename):
    """Load names from a JSON file"""
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)['sets']
    sets = []
    for set in data:
        count = str(len(set['flashcards']))
        sets.append((set['title'], count, set['description'], set['tags'], set['id']))
    return sets

def get_object_by_id(data, id):
    
    for set in data:
        if set.get('id') == id:
            return set
    raise ValueError(f'Set with id {id} not found in {data}')

if __name__ == '__main__':
    print(load_sets('flashcards.json'))