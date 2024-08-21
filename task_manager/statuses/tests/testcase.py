from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.helpers import load_data, remove_rollbar

User = get_user_model()


@remove_rollbar
class StatusTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    test_status = load_data('test_status.json')

    def setUp(self):
        self.client = Client()
        user = User.objects.get(pk=1)
        self.client.force_login(user)
        self.statuses = Status.objects.all()
        self.count = Status.objects.count()
