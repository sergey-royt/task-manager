from task_manager.tasks.models import Task
from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.statuses.models import Status


User = get_user_model()


class TestTaskInstanceCreate(TestCase):
    fixtures = ["users.json", "statuses.json"]

    def test_create_instance(self):
        self.assertEqual(Task.objects.count(), 0)

        user = User.objects.get(pk=1)
        status = Status.objects.get(pk=1)

        credentials = {
            "name": "Update Company Website",
            "description": "Update the homepage of the website "
            "by adding new photos and information "
            "about the latest products. "
            "Ensure that all links are working correctly.",
            "status": 1,
            "executor": 1,
        }

        task = Task.objects.create(
            name=credentials["name"],
            description=credentials["description"],
            author=user,
            status=status,
        )

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.name, credentials["name"])
        self.assertEqual(task.description, credentials["description"])
        self.assertEqual(task.author, user)
