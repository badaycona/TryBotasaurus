import json
import os

def save_json(filename, data):
    os.makedirs('output', exist_ok=True)
    path = os.path.join('output', filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
