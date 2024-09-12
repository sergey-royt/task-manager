from .testcase import StatusTestCase
from django.urls import reverse
from http import HTTPStatus


class TestStatusListView(StatusTestCase):
    """Test Status index view"""

    def test_not_authenticated_access(self) -> None:
        """Test not authenticated access
        check status code and redirect to login page"""

        self.client.logout()
        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_authenticated_access(self) -> None:
        """Test authenticated access
        check status code and template used"""

        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_content(self) -> None:
        """
        Test page content
        Check all Statuses are shown
        """

        response = self.client.get(reverse('status_index'))
        self.assertEqual(response.context['statuses'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['statuses'],
            self.statuses,
            ordered=False
        )


class TestStatusCreateView(StatusTestCase):
    """Test Status create view"""

    def test_status_create_view_not_authenticated(self) -> None:
        """
        Test status create not authenticated
        Check status code, redirect to login page.
        """

        self.client.logout()
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_create_view(self) -> None:
        """
        Test status create authenticated
        Check status code, template used
        """

        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestStatusUpdateView(StatusTestCase):
    """Test Status update view"""

    def test_status_update_view_not_authenticated(self) -> None:
        """
        Test status update not authenticated
        Check status code, redirect to login page.
        """

        self.client.logout()
        response = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_update_view(self) -> None:
        """
        Test status update authenticated
        Check status code, template used.
        """

        response = self.client.get(reverse('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestStatusDeleteView(StatusTestCase):
    def test_status_delete_view_not_authenticated(self) -> None:
        """
        Test status delete not authenticated
        Check status code, redirect to login page.
        """

        self.client.logout()
        response = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_delete_view(self) -> None:
        """
        Test status delete authenticated
        Check status code, template used.
        """

        response = self.client.get(reverse('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/delete.html')
