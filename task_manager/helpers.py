import json
import os


def load_data(path):
    with open(os.path.abspath(f'task_manager/{path}'), 'r') as file:
        return json.loads(file.read())
