import json
import os
from django.test import modify_settings


def load_data(path):
    with open(os.path.abspath(f'task_manager/{path}'), 'r') as file:
        return json.loads(file.read())


remove_rollbar = modify_settings(
    MIDDLEWARE={
        "remove":
            ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware']
    }
)
