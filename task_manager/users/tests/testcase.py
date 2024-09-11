from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.helpers import load_data

User = get_user_model()


class UserTestCase(TestCase):
    """
    Test Case inherits django TestCase
    Make test database with users, statuses, tasks and labels data
    load data for tests and put it in test_user variable"""

    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    test_user = load_data('users/tests/fixtures/test_user.json')

    def setUp(self) -> None:
        """Set up test client and 3 users from test db
        initialize self count value which is 3
        make a force login with user1 credentials"""

        self.users = User.objects.all()
        self.user1 = self.users.get(pk=1)
        self.user2 = self.users.get(pk=2)
        self.user3 = self.users.get(pk=3)
        self.count = User.objects.count()

        self.client = Client()
        self.client.force_login(self.user1)
