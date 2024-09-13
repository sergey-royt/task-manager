from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label

from django.test import TestCase


class TestLabelForm(TestCase):
    def test_label_form_valid(self) -> None:

        data = {"name": "enhancement"}
        form = LabelForm(data=data)

        self.assertTrue(form.is_valid())

    def test_label_form_missing_field(self) -> None:

        data = {"name": ""}
        form = LabelForm(data=data)

        self.assertFalse(form.is_valid())

    def test_label_form_exists(self) -> None:
        Label.objects.create(name="bug")

        data = {"name": "bug"}
        form = LabelForm(data=data)

        self.assertFalse(form.is_valid())
