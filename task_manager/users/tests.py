from django.test import TestCase, Client
from django.urls import reverse


class UsersTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test(self):
        self._test_users_list()

    def _test_users_list(self):
        response = self.client.get(reverse('users_index'))
        self.assertIn('users', response.context)
