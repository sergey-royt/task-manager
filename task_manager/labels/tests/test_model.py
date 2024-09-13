from task_manager.labels.models import Label
from django.test import TestCase


class TestLabelModel(TestCase):

    def test_label_model(self) -> None:
        self.assertQuerySetEqual(Label.objects.all(), [])
        count = Label.objects.count()

        test_label = {"name": "enhancement"}
        label = Label.objects.create(**test_label)

        self.assertEqual(Label.objects.count(), count + 1)
        self.assertEqual(label.name, test_label["name"])
