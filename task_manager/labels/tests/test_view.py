from http import HTTPStatus
from .testcase import LabelTestCase
from django.urls import reverse


class TestLabelIndexView(LabelTestCase):
    """Test Label index view"""

    def test_label_index_view(self) -> None:
        """
        Test authenticated access
        check status code and template used
        """

        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/index.html')

    def test_label_index_view_not_authenticated(self) -> None:
        """
        Test not authenticated access
        check status code and redirect to login page
        """

        self.client.logout()
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_label_index_view_content(self) -> None:
        """
        Test page content
        Check all Labels objects are shown
        """

        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.context['labels'].count(), self.count)
        self.assertQuerysetEqual(
            response.context['labels'],
            self.labels,
            ordered=False
        )


class TestLabelCreateView(LabelTestCase):
    """Test Label create view"""

    def test_label_create_view(self) -> None:
        """
        test proper status code and template is used
        """

        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_label_index_view_not_authenticated(self) -> None:
        """
        test proper status code and redirect to login page
        """

        self.client.logout()
        response = self.client.get(reverse('labels_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))


class TestLabelUpdateView(LabelTestCase):
    """Test Label update view"""

    def test_label_update_view_not_authenticated(self) -> None:
        """
        test proper status code and redirect to login page
        """

        self.client.logout()
        response = self.client.get(reverse('labels_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_status_update_view(self) -> None:
        """
        Test proper status code and template
        """

        response = self.client.get(reverse('labels_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')


class TestLabelDeleteView(LabelTestCase):
    """Test Label delete view"""

    def test_label_delete_view_not_authenticated(self) -> None:
        """
        Test Label delete view not authenticated
        Check status code and redirect to login page
        """

        self.client.logout()
        response = self.client.get(reverse('labels_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))

    def test_label_delete_view(self) -> None:
        """
        Test proper status code and template is used
        """

        response = self.client.get(reverse('labels_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/delete.html')
