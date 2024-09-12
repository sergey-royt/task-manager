from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.helpers import load_data
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


User = get_user_model()


class TaskTestCase(TestCase):
    """
        Test Case inherits django TestCase
        Make test database with users, statuses, tasks and labels data
        load data for tests and put it in test_task variable"""

    fixtures = ['statuses.json', 'tasks.json', 'users.json', 'labels.json']
    test_task = load_data('tasks/tests/fixtures/test_task.json')

    def setUp(self) -> None:
        """
        Set up test client, 2 tasks and user from test db
        initialize self count value which is 2
        make a force login with user credentials
        """

        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.tasks = Task.objects.all()
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.count = Task.objects.count()

        self.client.force_login(self.user)
