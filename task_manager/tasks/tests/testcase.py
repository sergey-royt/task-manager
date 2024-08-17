from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.helpers import load_data
from task_manager.tasks.models import Task


User = get_user_model()


class TaskTestCase(TestCase):
    fixtures = ['statuses.json', 'tasks.json', 'users.json']
    test_task = load_data('test_task.json')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)
        self.count = Task.objects.count()

        self.client.force_login(self.user)
