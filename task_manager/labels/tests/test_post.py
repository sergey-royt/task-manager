from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from http import HTTPStatus

from task_manager.labels.models import Label


User = get_user_model()


class TestLabelCreate(TestCase):

    def test_create_not_authenticated(self) -> None:
        self.assertQuerySetEqual(Label.objects.all(), [])

        valid_label = {
            "name": "enhancement"
        }

        response = self.client.post(
            reverse('labels_create'), data=valid_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertQuerySetEqual(Label.objects.all(), [])

    def test_create_authenticated(self) -> None:
        self.assertQuerySetEqual(Label.objects.all(), [])

        count = Label.objects.count()

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        valid_label = {
            "name": "enhancement"
        }

        self.client.force_login(user)
        response = self.client.post(
            reverse('labels_create'), data=valid_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), count + 1)
        self.assertQuerySetEqual(
            Label.objects.last().name, valid_label['name']
        )

    def test_create_empty(self) -> None:
        self.assertQuerySetEqual(Label.objects.all(), [])

        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        empty_label = {"name": ""}

        self.client.force_login(user)
        response = self.client.post(
            reverse('labels_create'), data=empty_label
        )

        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(Label.objects.all(), [])

    def test_create_exists(self) -> None:
        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        existing_label = {"name": "bug"}

        Label.objects.create(**existing_label)
        count = Label.objects.count()

        self.client.force_login(user)
        response = self.client.post(
            reverse('labels_create'), data=existing_label
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Label with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Label.objects.count(), count)


class TestLabelUpdate(TestCase):

    def test_update_not_authenticated(self) -> None:
        label = Label.objects.create(name="bug")

        update_label = {"name": "help wanted"}

        response = self.client.post(
            reverse(
                'labels_update', kwargs={'pk': label.pk}), data=update_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertNotEqual(Label.objects.get(pk=label.pk).name, update_label)

    def test_update(self) -> None:
        user = User.objects.create_user(
            {'username': 'username', 'password': 'G00d_pa$$w0rd'}
        )

        update_label = {"name": "help wanted"}

        label = Label.objects.create(name="bug")
        count = Label.objects.count()

        self.client.force_login(user)
        response = self.client.post(
            reverse(
                'labels_update', kwargs={'pk': label.pk}), data=update_label
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), count)
        self.assertQuerySetEqual(
            Label.objects.get(pk=label.pk).name, update_label['name']
        )


class TestLabelDelete(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def test_delete_label_not_authenticated(self) -> None:
        count = Label.objects.count()

        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Label.objects.count(), count)

    def test_delete_label(self) -> None:
        user = User.objects.get(pk=1)
        count = Label.objects.count()

        self.client.force_login(user)
        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=3)

    def test_delete_bound_label(self) -> None:
        user = User.objects.get(pk=1)
        count = Label.objects.count()

        self.client.force_login(user)

        response = self.client.post(
            reverse('labels_delete', kwargs={'pk': 1})
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(
            str(messages[0]), _('Cannot delete label because it in use')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('labels_index'))
        self.assertEqual(Label.objects.count(), count)
