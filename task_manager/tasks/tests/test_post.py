from .testcase import TaskTestCase
from django.urls import reverse
from http import HTTPStatus
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class TestTaskCreate(TaskTestCase):
    def test_task_create_valid(self):
        task_data = self.test_task['create']['valid'].copy()
        response = self.client.post(reverse('task_create'), data=task_data)
        created_task = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(created_task.name, task_data['name'])
        self.assertEqual(created_task.author, self.user)
        self.assertEqual(created_task.executor, self.user)

    def test_task_create_missing_field(self):
        task_data = self.test_task['create']['missing_field'].copy()
        response = self.client.post(reverse('task_create'), data=task_data)
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('description', errors)
        self.assertEqual(
            [error_help],
            errors['description']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Task.objects.count(), self.count)
        self.assertNotEqual(Task.objects.last().author, self.user)

    def test_create_task_exists(self):
        existing_task = self.test_task['create']['exists'].copy()
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
        self.assertEqual(Task.objects.count(), self.count)


class TestTaskUpdate(TaskTestCase):
    def test_task_update(self):
        update_task = self.test_task['update'].copy()
        response = self.client.post(
            reverse('task_update', kwargs={'pk': 1}), data=update_task
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), self.count)
        self.assertQuerySetEqual(
            Task.objects.get(pk=1).name, update_task['name']
        )
