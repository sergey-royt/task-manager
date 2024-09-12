from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from task_manager.helpers import load_data
from task_manager.labels.models import Label


User = get_user_model()


class LabelTestCase(TestCase):
    """
    Test Case inherits django TestCase
    Make test database with users, statuses, tasks and labels data
    load data for tests and put it in test_labels variable
    """

    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']
    test_labels = load_data('labels/tests/fixtures/test_labels.json')

    def setUp(self):
        """
        Set up test Client, 3 labels and user from test db
        initialize self count value which is 3
        make a force login with user credentials
        """

        self.labels = Label.objects.all()
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.user = User.objects.get(pk=1)
        self.count = Label.objects.count()

        self.client = Client()
        self.client.force_login(self.user)
