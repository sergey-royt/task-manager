from http import HTTPStatus

from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.users.tests.factories.user_factory import UserFactory

User = get_user_model()


class TestUserListView(TestCase):
    fixtures = ["users.json"]

    def test_access_and_content(self) -> None:
        count = User.objects.count()
        users = User.objects.all()

        response = self.client.get(reverse("users_index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/index.html")
        self.assertEqual(response.context["users"].count(), count)
        self.assertQuerysetEqual(
            response.context["users"], users, ordered=False
        )

    def test_1_db_queries_logout(self) -> None:
        for _ in range(10):
            UserFactory()

        with self.assertNumQueries(1):
            self.client.get(reverse("users_index"))

    def test_3_db_queries_login(self) -> None:
        user = UserFactory()
        self.client.force_login(user)

        with self.assertNumQueries(3):
            self.client.get(reverse("users_index"))


class TestUserCreateView(TestCase):

    def test_view_access(self) -> None:

        response = self.client.get(reverse("users_create"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "form.html")


class TestUserUpdateView(TestCase):

    def test_view_update_not_authenticated(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        response = self.client.get(
            reverse("users_update", kwargs={"pk": user.pk})
        )

        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertRedirects(response, reverse("login"))

    def test_view_update_self(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("users_update", kwargs={"pk": user.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "form.html")

    def test_view_update_other(self) -> None:
        user1 = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        user2 = User.objects.create_user(
            {"username": "test", "password": "$ecurE_paSSw0rD"}
        )

        self.client.force_login(user1)

        response = self.client.get(
            reverse_lazy("users_update", kwargs={"pk": user2.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))


class TestUserDeleteView(TestCase):

    def test_view_delete_not_authenticated(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        response = self.client.get(
            reverse("users_delete", kwargs={"pk": user.pk})
        )

        self.assertFalse(response.status_code == HTTPStatus.OK)
        self.assertRedirects(response, reverse("login"))

    def test_view_delete_self(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        self.client.force_login(user)

        response = self.client.get(
            reverse("users_delete", kwargs={"pk": user.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/delete.html")

    def test_view_delete_other(self) -> None:
        user1 = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )
        user2 = User.objects.create_user(
            {"username": "test", "password": "$ecurE_paSSw0rD"}
        )

        self.client.force_login(user1)

        response = self.client.get(
            reverse_lazy("users_delete", kwargs={"pk": user2.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users_index"))
