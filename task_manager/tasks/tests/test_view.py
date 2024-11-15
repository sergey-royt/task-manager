from django.shortcuts import reverse
from http import HTTPStatus
from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.labels.tests.factories.label_factory import LabelFactory
from task_manager.tasks.models import Task
from task_manager.tasks.tests.factories.task_factory import TaskFactory
from task_manager.users.tests.factories.user_factory import UserFactory

User = get_user_model()


class TestTaskIndexView(TestCase):
    fixtures = ["users.json", "labels.json", "statuses.json", "tasks.json"]

    def test_access_and_content(self) -> None:

        response = self.client.get(reverse("task_index"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("login"))

        user = User.objects.get(pk=1)

        self.client.force_login(user)

        response = self.client.get(reverse("task_index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertEqual(
            response.context["tasks"].count(), Task.objects.count()
        )
        self.assertQuerysetEqual(
            response.context["tasks"], Task.objects.all(), ordered=False
        )

    def test_7_db_queries_login(self) -> None:
        user = UserFactory()
        self.client.force_login(user)

        for _ in range(20):
            label = LabelFactory()
            task = TaskFactory()
            task.labels.set([label])

        with self.assertNumQueries(7):
            self.client.get(reverse("task_index"))

    def test_filter(self) -> None:
        user = User.objects.get(pk=1)

        self.client.force_login(user)

        response = self.client.get(reverse("task_index"), {"status": 1})

        self.assertEqual(response.context["tasks"].count(), 1)
        self.assertContains(response, Task.objects.get(pk=1))
        self.assertNotContains(response, Task.objects.get(pk=2))


class TestTaskCreateView(TestCase):

    def test_task_create_view_access(self) -> None:
        user = User.objects.create_user(
            {"username": "username", "password": "G00d_pa$$w0rd"}
        )

        response1 = self.client.get(reverse("task_create"))

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse("login"))

        self.client.force_login(user)

        response2 = self.client.get(reverse("task_create"))

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, "form.html")


class TestTaskUpdateView(TestCase):
    fixtures = ["users.json", "labels.json", "statuses.json", "tasks.json"]

    def test_task_update_view_access(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=1)

        response1 = self.client.get(
            reverse("task_update", kwargs={"pk": task.pk})
        )

        self.assertEqual(response1.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response1, reverse("login"))

        self.client.force_login(user)

        response2 = self.client.get(
            reverse("task_update", kwargs={"pk": task.pk})
        )

        self.assertEqual(response2.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response2, "form.html")


class TestTaskDeleteView(TestCase):
    fixtures = ["users.json", "labels.json", "statuses.json", "tasks.json"]

    def test_task_view_delete_own(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=1)

        self.client.force_login(user)

        response = self.client.get(
            reverse("task_delete", kwargs={"pk": task.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/delete.html")

    def test_task_view_delete_other(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=2)

        self.client.force_login(user)

        response = self.client.get(
            reverse("task_delete", kwargs={"pk": task.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("task_index"))


class TestTaskDetailView(TestCase):
    fixtures = ["users.json", "labels.json", "statuses.json", "tasks.json"]

    def test_task_detail_view_access(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=2)

        self.client.force_login(user)

        response = self.client.get(
            reverse("task_details", kwargs={"pk": task.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/details.html")
        self.assertContains(response, task.name)
        self.assertContains(response, task.description)

    def test_4_db_queries(self) -> None:
        user = UserFactory()
        self.client.force_login(user)

        task = TaskFactory()

        with self.assertNumQueries(4):
            self.client.get(reverse("task_details", kwargs={"pk": task.pk}))
