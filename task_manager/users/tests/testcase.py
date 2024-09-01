from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.helpers import load_data, remove_rollbar

User = get_user_model()


@remove_rollbar
class UserTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    test_user = load_data('users/tests/fixtures/test_user.json')

    def setUp(self):
        self.users = User.objects.all()
        self.user1 = self.users.get(pk=1)
        self.user2 = self.users.get(pk=2)
        self.user3 = self.users.get(pk=3)
        self.count = User.objects.count()

        self.client = Client()
        self.client.force_login(self.user1)
