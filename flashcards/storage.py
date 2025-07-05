import json
import uuid

FILENAME = 'flashcards.json'

def get_data(filename) -> list[dict]:
    """Read 'sets' data from the given JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file).get('sets', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {filename}: {e}")
        return []
    
def save_data(filename, sets: list[dict]) -> bool:
    """Save all sets data to the given JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump({'sets': sets}, file, ensure_ascii=False, indent=4)
            return True
    except IOError as e:
        print(f"Error saving to {filename}: {e}")
        return False
        
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

def load_sets(filename) -> list[tuple[str]]:
    """Load names from a JSON file"""
    data = get_data(filename)
    sets = []
    for item in data:
        count = str(len(item['flashcards']))
        sets.append((item['title'], count, item['description'], item['tags'], item['id']))
    return sets

def get_set_by_id(filename, id: int | str) -> dict:
    """Get a set by its ID from the JSON file."""
    data = get_data(filename)
    for item in data:
        if item.get('id') == id:
            return item
    raise ValueError(f'Set with id {id} not found in {data}')

def remove_set(filename, id):
    """Remove a set by its ID from the JSON file."""
    data = get_data(filename)
    item = get_set_by_id(filename, id)
    data.remove(item)
    save_data(filename, data)

if __name__ == '__main__':
    print(get_set_by_id(FILENAME, "d19fcd00-cc71-41e2-b42e-19ccbeefae6e"))