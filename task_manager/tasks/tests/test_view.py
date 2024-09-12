from .testcase import TaskTestCase
from django.shortcuts import reverse
from http import HTTPStatus


class TestTaskIndexView(TaskTestCase):
    """Test Task index view"""

    def test_access_not_authenticated(self) -> None:
        """
        Test not authenticated access
        check status code and redirect address
        """

        self.client.logout()
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_access(self) -> None:
        """Test authenticated access
        check status code and used template"""

        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_content(self) -> None:
        """
        Test page content without any filters
        Check all Task objects are shown
        """

        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.context['tasks'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['tasks'],
            self.tasks,
            ordered=False
        )

    def test_filter(self) -> None:
        """Test page content with status filter
        Check count of tasks shown
        Check only proper task shown"""
        response = self.client.get(reverse('task_index'), {'status': 1})
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)


class TestTaskCreateView(TaskTestCase):
    """Test Task create view"""

    def test_task_create_view_access(self) -> None:
        """test proper status code and template is used"""

        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_task_create_view_access_not_authenticated(self) -> None:
        """test proper status code and redirect to log in page"""

        self.client.logout()
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))


class TestTaskUpdateView(TaskTestCase):
    """Test Task update view"""

    def test_task_update_view_not_authenticated(self) -> None:
        """test proper status code and redirect to log in page"""

        self.client.logout()
        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_update_view(self) -> None:
        """Test proper status code and template trying update authenticated"""

        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestTaskDeleteView(TaskTestCase):
    """Test Task delete view"""

    def test_task_view_delete_own(self) -> None:
        """Test proper status code and template values
        trying to delete own task"""

        response = self.client.get(reverse('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/delete.html')

    def test_task_view_delete_other(self) -> None:
        """
        Test proper status code and redirect to task index page
        trying to delete task created by other user
        """

        response = self.client.get(
            reverse('task_delete', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('task_index'))


class TestTaskDetailView(TaskTestCase):
    """Test Task detail view"""

    def test_task_detail_view_access(self) -> None:
        """
        Test Task detail view authenticated
        Check status code, used template,
        task name and description accuracy
        """

        response = self.client.get(reverse('task_details', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/details.html')
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task1.description)
