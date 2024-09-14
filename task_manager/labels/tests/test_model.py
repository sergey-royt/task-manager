from task_manager.labels.models import Label
from django.test import TestCase


class TestLabelModel(TestCase):

    def test_label_model(self) -> None:
        self.assertEqual(Label.objects.count(), 0)

        test_label = {"name": "enhancement"}
        label = Label.objects.create(**test_label)

        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(label.name, test_label["name"])
