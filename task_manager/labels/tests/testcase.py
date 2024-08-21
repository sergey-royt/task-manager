from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from task_manager.helpers import load_data, remove_rollbar
from task_manager.labels.models import Label


User = get_user_model()


@remove_rollbar
class LabelTestCase(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']
    test_labels = load_data('test_labels.json')

    def setUp(self):
        self.labels = Label.objects.all()
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.user = User.objects.get(pk=1)
        self.count = Label.objects.count()

        self.client = Client()
        self.client.force_login(self.user)
