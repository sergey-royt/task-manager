from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.statuses.models import Status

User = get_user_model()


class TestStatusListView(TestCase):
    fixtures = ["statuses.json"]

    def test_access_and_content(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        count = Status.objects.count()

        response1 = self.client.get(reverse("status_index"))

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse("login"))

        self.client.force_login(user)

        response2 = self.client.get(reverse("status_index"))

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, "statuses/index.html")

        self.assertEqual(response2.context["statuses"].count(), count)
        self.assertQuerysetEqual(
            response2.context["statuses"], Status.objects.all(), ordered=False
        )


class TestStatusCreateView(TestCase):

    def test_status_create_view_access(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        response1 = self.client.get(reverse("status_create"))

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse("login"))

        self.client.force_login(user)

        response2 = self.client.get(reverse("status_create"))

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, "form.html")


class TestStatusUpdateView(TestCase):
    fixtures = ["statuses.json"]

    def test_status_update_view_not_authenticated(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        response1 = self.client.get(reverse("status_update", kwargs={"pk": 1}))

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse("login"))

        self.client.force_login(user)

        response2 = self.client.get(reverse("status_update", kwargs={"pk": 1}))

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, "form.html")


class TestStatusDeleteView(TestCase):
    fixtures = ["statuses.json"]

    def test_status_delete_view_access(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        response1 = self.client.get(reverse("status_delete", kwargs={"pk": 1}))

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse("login"))

        self.client.force_login(user)

        response2 = self.client.get(reverse("status_delete", kwargs={"pk": 1}))

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, "statuses/delete.html")
