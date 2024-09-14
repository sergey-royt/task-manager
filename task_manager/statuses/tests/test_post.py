from django.urls import reverse
from http import HTTPStatus
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status


User = get_user_model()


class TestCreateStatus(TestCase):
    def test_create_not_authenticated(self) -> None:
        self.assertEqual(Status.objects.count(), 0)

        valid_status = {"name": "Paused"}

        response = self.client.post(
            reverse("status_create"), data=valid_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(Status.objects.count(), 0)

    def test_create_authenticated(self) -> None:
        self.assertEqual(Status.objects.count(), 0)

        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        valid_status = {"name": "Paused"}

        self.client.force_login(user)

        response = self.client.post(
            reverse("status_create"), data=valid_status
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("status_index"))
        self.assertEqual(Status.objects.count(), 1)
        self.assertQuerySetEqual(
            Status.objects.last().name, valid_status["name"]
        )

    def test_create_empty(self) -> None:
        self.assertEqual(Status.objects.count(), 0)

        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        empty_status = {"name": ""}

        self.client.force_login(user)
        response = self.client.post(
            reverse("status_create"), data=empty_status
        )

        errors = response.context["form"].errors
        error_help = _("This field is required.")

        self.assertIn("name", errors)
        self.assertEqual([error_help], errors["name"])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Status.objects.count(), 0)

    def test_create_exists(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        status_data = {"name": "New"}
        self.assertEqual(Status.objects.count(), 0)
        Status.objects.create(**status_data)
        self.assertEqual(Status.objects.count(), 1)

        self.client.force_login(user)
        response = self.client.post(reverse("status_create"), data=status_data)

        errors = response.context["form"].errors

        self.assertIn("name", errors)
        self.assertEqual(
            [_("Status with this Name already exists.")], errors["name"]
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Status.objects.count(), 1)


class TestUpdateStatus(TestCase):

    def test_update_not_authenticated(self) -> None:
        status_data = {"name": "New"}
        status = Status.objects.create(name="Archived")

        response = self.client.post(
            reverse("status_update", kwargs={"pk": status.pk}),
            data=status_data,
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("login"))
        self.assertNotEqual(
            Status.objects.get(pk=status.pk).name, status_data["name"]
        )

    def test_update(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        status_data = {"name": "New"}
        self.assertEqual(Status.objects.count(), 0)
        status = Status.objects.create(name="Bug")
        self.assertEqual(Status.objects.count(), 1)

        self.client.force_login(user)
        response = self.client.post(
            reverse("status_update", kwargs={"pk": status.pk}),
            data=status_data,
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("status_index"))
        self.assertEqual(Status.objects.count(), 1)
        self.assertQuerySetEqual(
            Status.objects.get(pk=status.pk).name, status_data["name"]
        )


class TestDeleteStatus(TestCase):
    fixtures = ["users.json", "statuses.json", "tasks.json", "labels.json"]

    def test_delete_status_not_authenticated(self) -> None:
        count = Status.objects.count()

        response = self.client.post(reverse("status_delete", kwargs={"pk": 3}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(Status.objects.count(), count)

    def test_delete_status(self) -> None:
        user = User.objects.get(pk=1)
        count = Status.objects.count()

        self.client.force_login(user)
        response = self.client.post(reverse("status_delete", kwargs={"pk": 3}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("status_index"))
        self.assertEqual(Status.objects.count(), count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=3)

    def test_delete_bound_status(self) -> None:
        user = User.objects.get(pk=1)
        count = Status.objects.count()

        self.client.force_login(user)
        response = self.client.post(reverse("status_delete", kwargs={"pk": 1}))

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]), _("Cannot delete status because it in use")
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("status_index"))
        self.assertEqual(Status.objects.count(), count)
