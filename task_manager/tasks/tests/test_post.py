from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from http import HTTPStatus
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestTaskCreate(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def test_task_create_valid(self) -> None:
        user = User.objects.get(pk=1)
        count = Task.objects.count()

        task_data = {
            "name": "Update Company Website",
            "description": "Update the homepage of the website by "
                           "adding new photos and information about "
                           "the latest products. Ensure that all links "
                           "are working correctly.",
            "status": 1,
            "executor": 1
        }

        self.client.force_login(user)
        response = self.client.post(reverse('task_create'), data=task_data)

        created_task = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), count + 1)
        self.assertEqual(created_task.name, task_data['name'])
        self.assertEqual(created_task.author, user)
        self.assertEqual(created_task.executor, user)

    def test_task_create_missing_field(self) -> None:
        user = User.objects.get(pk=1)
        count = Task.objects.count()

        task_data = {
            "name": "Update Company Website",
            "executor": 1,
            "status": 1
        }
        self.client.force_login(user)
        response = self.client.post(reverse('task_create'), data=task_data)

        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('description', errors)
        self.assertEqual(
            [error_help],
            errors['description']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Task.objects.count(), count)
        self.assertNotEqual(Task.objects.last().author, user)

    def test_create_task_exists(self) -> None:
        user = User.objects.get(pk=1)
        count = Task.objects.count()

        existing_task = {
            "name": "Prepare Sales Report",
            "description": "Collect data on sales for the last "
                           "quarter and prepare a detailed report "
                           "for the team meeting.",
            "status": 1
        }

        self.client.force_login(user)
        response = self.client.post(
            reverse('task_create'), data=existing_task
        )

        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Task with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Task.objects.count(), count)


class TestTaskUpdate(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def test_task_update(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=1)
        count = Task.objects.count()

        update_task = {
            "name": "Update Company Website",
            "description": "Update the homepage of the website by adding "
                           "new photos and information about the latest "
                           "products. "
                           "Ensure that all links are working correctly.",
            "status": 1,
            "executor": 1
        }

        self.client.force_login(user)
        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.pk}), data=update_task
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), count)
        self.assertQuerySetEqual(
            Task.objects.get(pk=task.pk).name, update_task['name']
        )


class TestTaskDelete(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def test_delete_task_not_authenticated(self) -> None:
        count = Task.objects.count()

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Task.objects.count(), count)

    def test_delete_task_own(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=1)
        count = Task.objects.count()

        self.client.force_login(user)
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=1)

    def test_delete_task_foreign(self) -> None:
        user = User.objects.get(pk=1)
        task = Task.objects.get(pk=2)
        count = Task.objects.count()

        self.client.force_login(user)

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.pk})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), count)
