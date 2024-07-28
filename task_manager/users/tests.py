from django.test import TestCase, Client
from faker import Faker
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
# Create your tests here.

User = get_user_model()

class UsersTest(TestCase):
    def create_user(self):
        self.client = Client()
        self.faker = Faker()
        self.username = self.faker.user_name()
        self.password = self.faker.password(length=10)
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.user.save()

    def test_create(self):
        response = self.client.post(reverse_lazy('create_user'), data={'username': self.username,
                                                                       'password': self.password})

