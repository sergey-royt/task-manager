from .testcase import TaskTestCase
from django.shortcuts import reverse
from http import HTTPStatus


class TestTaskIndexView(TaskTestCase):
    def test_access_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_access(self):
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_content(self):
        response = self.client.get(reverse('task_index'))
        self.assertEqual(response.context['tasks'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['tasks'],
            self.tasks,
            ordered=False
        )

    def test_filter(self):
        response = self.client.get(reverse('task_index'), {'status': 1})
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)


class TestTaskCreateView(TaskTestCase):
    def test_task_create_view_access(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_task_create_view_access_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))


class TestTaskUpdateView(TaskTestCase):
    def test_task_update_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_update_view(self):
        response = self.client.get(reverse('task_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')
