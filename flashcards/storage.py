import json
import uuid

FILENAME = 'flashcards.json'

def get_data(filename):
    """Read 'sets' data from the given JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file).get('sets', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {filename}: {e}")
        return []
    
def save_data(filename, sets):
    """Save all sets data to the given JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump({'sets': sets}, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving to {filename}: {e}")
        
def save_to_file(filename, **items):
    """Save a set to a JSON file."""
    data = get_data(filename)

    if items['id'] is None:
        items['id'] = str(uuid.uuid4())
        data.append(items)
    else:
        set = get_set_by_id(filename, items['id'])
        idx = data.index(set)
        data[idx] = items

    save_data(filename, data)

def load_sets(filename):
    """Load names from a JSON file"""
    data = get_data(filename)
    sets = []
    for set in data:
        count = str(len(set['flashcards']))
        sets.append((set['title'], count, set['description'], set['tags'], set['id']))
    return sets

def get_set_by_id(filename, id):
    """Get a set by its ID from the JSON file."""
    data = get_data(filename)
    for set in data:
        if set.get('id') == id:
            return set
    raise ValueError(f'Set with id {id} not found in {data}')

def remove_set(filename, id):
    """Remove a set by its ID from the JSON file."""
    data = get_data(filename)
    set = get_set_by_id(filename, id)
    data.remove(set)
    save_data(filename, data)

if __name__ == '__main__':
    print(get_set_by_id(FILENAME, "279fd33c-e33e-49e1-a08e-1811ecd18636"))