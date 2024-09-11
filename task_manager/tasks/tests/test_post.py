from django.core.exceptions import ObjectDoesNotExist
from .testcase import TaskTestCase
from django.urls import reverse
from http import HTTPStatus
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class TestTaskCreate(TaskTestCase):
    """Test Task create"""

    def test_task_create_valid(self) -> None:
        """
        Test create task with valid credentials
        Check status code, redirect to task index page,
        increase Task object count by one, task
        name, author and executor accuracy
        """

        task_data = self.test_task['create']['valid'].copy()
        response = self.client.post(reverse('task_create'), data=task_data)
        created_task = Task.objects.last()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(created_task.name, task_data['name'])
        self.assertEqual(created_task.author, self.user)
        self.assertEqual(created_task.executor, self.user)

    def test_task_create_missing_field(self) -> None:
        """
        Test create Task with missing field 'description'
        Check 'description' error in response,
        has 'field required' message.
        Check status code, object count not changed,
        last object author has remained the same
        """

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

    def test_create_task_exists(self) -> None:
        """
        Test create Task with existed 'name'
        Check 'name' error in response, has
        'task already exists' message.
        Check status code and Task object count
        not changed
        """

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
    """Test Task update"""

    def test_task_update(self) -> None:
        """
        Test Task update with proper credentials
        check status code, redirect to task index page,
        Task count not changed,
        task name has been changed
        """

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


class TestTaskDelete(TaskTestCase):
    """Test Task delete"""

    def test_delete_task_not_authenticated(self) -> None:
        """
        Test Task dekete not authenticated
        Check status code, redirect to log in page,
        Task object count not changed
        """

        self.client.logout()

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Task.objects.count(), self.count)

    def test_delete_task_own(self) -> None:
        """
        Test delete own Task
        Check status code, redirect to task index page,
        Task object count reduce by one,
        Task object does not exist.
        """

        response = self.client.post(
            reverse('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=1)

    def test_delete_task_foreign(self) -> None:
        """
        Test delete task created by other user
        Check status code, redirect to task index page,
        Task object count not changed
        """
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))
        self.assertEqual(Task.objects.count(), self.count)
