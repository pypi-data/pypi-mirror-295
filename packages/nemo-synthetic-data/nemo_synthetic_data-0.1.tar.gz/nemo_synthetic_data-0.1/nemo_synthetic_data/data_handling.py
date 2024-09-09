import json
import jsonlines
import sys

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def save_jsonl(data, file_path, encoding='utf-8'):
    with jsonlines.open(file_path, mode='w') as writer:
        for item in data:
            writer.write(item)