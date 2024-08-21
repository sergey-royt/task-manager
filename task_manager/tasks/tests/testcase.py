from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.helpers import load_data, remove_rollbar
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


User = get_user_model()


@remove_rollbar
class TaskTestCase(TestCase):
    fixtures = ['statuses.json', 'tasks.json', 'users.json', 'labels.json']
    test_task = load_data('test_task.json')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.tasks = Task.objects.all()
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.count = Task.objects.count()

        self.client.force_login(self.user)
