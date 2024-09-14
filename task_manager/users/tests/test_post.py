from django.contrib.messages import get_messages
from django.test import TestCase
from django.shortcuts import reverse
from http import HTTPStatus
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class TestUserCreate(TestCase):

    def test_user_create_valid(self) -> None:
        self.assertEqual(User.objects.count(), 0)

        credentials = {
            "first_name": "Malika",
            "last_name": "Hodkiewicz",
            "username": "malika-hodkiewicz",
            "password1": "8RvGr5wWTu",
            "password2": "8RvGr5wWTu",
        }
        response = self.client.post(reverse("users_create"), data=credentials)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, credentials["username"])

    def test_user_create_missing_field(self) -> None:
        self.assertEqual(User.objects.count(), 0)

        credentials = {
            "first_name": "John",
            "last_name": "Doe",
            "password1": "S3cur3P@ssw0rd!",
            "password2": "S3cur3P@ssw0rd!",
        }

        response = self.client.post(reverse("users_create"), data=credentials)

        errors = response.context["form"].errors
        error_help = _("This field is required.")

        self.assertIn("username", errors)
        self.assertEqual([error_help], errors["username"])
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), 0)

    def test_user_create_username_exists(self) -> None:
        self.assertEqual(User.objects.count(), 0)

        credentials = {
            "username": "alice_johnson",
            "first_name": "Alice",
            "last_name": "Johnson",
            "password1": "A!c3J0hn$on2024",
            "password2": "A!c3J0hn$on2024",
        }
        User.objects.create_user(
            username=credentials["username"], password=credentials["password1"]
        )

        self.assertEqual(User.objects.count(), 1)

        response = self.client.post(reverse("users_create"), data=credentials)

        errors = response.context["form"].errors
        error_help = _("A user with that username already exists.")

        self.assertIn("username", errors)
        self.assertEqual([error_help], errors["username"])

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(User.objects.count(), 1)


class TestUserUpdate(TestCase):

    def test_user_update_self(self) -> None:
        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        credentials = {
            "username": "michael789",
            "first_name": "Michael",
            "last_name": "Smith",
            "password1": "Str0ng!Passw0rd",
            "password2": "Str0ng!Passw0rd",
        }

        self.assertEqual(User.objects.count(), 1)

        self.client.force_login(user)

        response = self.client.post(
            reverse("users_update", kwargs={"pk": user.pk}), data=credentials
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            User.objects.get(pk=user.pk).first_name, credentials["first_name"]
        )

    def test_user_update_other(self) -> None:
        user1 = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        user2 = User.objects.create_user(
            {"username": "test", "password": "$ecurE_paSSw0rD"}
        )
        credentials = {
            "username": "michael789",
            "first_name": "Michael",
            "last_name": "Smith",
            "password1": "Str0ng!Passw0rd",
            "password2": "Str0ng!Passw0rd",
        }

        self.client.force_login(user1)

        response = self.client.post(
            reverse("users_update", kwargs={"pk": user2.pk}), data=credentials
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))
        self.assertNotEqual(
            User.objects.get(id=user2.pk).first_name, credentials["first_name"]
        )


class TestUserDelete(TestCase):
    fixtures = ["users.json", "statuses.json", "tasks.json", "labels.json"]

    def test_user_delete_self(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        count = User.objects.count()

        self.client.force_login(user)

        response = self.client.post(
            reverse("users_delete", kwargs={"pk": user.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))
        self.assertEqual(User.objects.count(), count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=user.pk)

    def test_user_delete_other(self) -> None:
        user1 = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        user2 = User.objects.create_user(
            {"username": "test", "password": "$ecurE_paSSw0rD"}
        )
        count = User.objects.count()

        self.client.force_login(user1)

        response = self.client.post(
            reverse("users_delete", kwargs={"pk": user2.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))
        self.assertEqual(User.objects.count(), count)

    def test_user_delete_bound(self) -> None:
        count = User.objects.count()
        user = User.objects.get(pk=1)

        self.client.force_login(user)
        response = self.client.post(
            reverse("users_delete", kwargs={"pk": user.pk})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]),
            _(
                "It is not possible to delete a user "
                "because it is being used"
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))
        self.assertEqual(User.objects.count(), count)
