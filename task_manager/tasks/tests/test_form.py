from django.test import TestCase
from task_manager.tasks.forms import TaskForm


class TestTaskForm(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def test_task_form_valid(self):

        credentials = {
            "name": "Update Company Website",
            "description": "Update the homepage of the website "
                           "by adding new photos and information "
                           "about the latest products. "
                           "Ensure that all links are working correctly.",
            "status": 1,
            "executor": 1
        }

        form = TaskForm(data=credentials)

        self.assertTrue(form.is_valid())

    def test_task_form_missing_field(self):

        credentials = {
            "name": "Update Company Website",
            "executor": 1,
            "status": 1
        }

        form = TaskForm(data=credentials)

        self.assertFalse(form.is_valid())
