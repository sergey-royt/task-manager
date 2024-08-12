from django.test import TestCase, Client
from django.urls import reverse
from faker import Faker
from http import HTTPStatus


class TestStatus(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        pass

    def test(self):
        ...
