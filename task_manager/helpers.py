"""project custom utils"""

import json
import os
from typing import Any


def load_data(path: str) -> Any:
    """
    :path: to Json file in project directory
    :return: python object with loaded data from file
    """
    with open(os.path.abspath(f'task_manager/{path}'), 'r') as file:
        return json.loads(file.read())
