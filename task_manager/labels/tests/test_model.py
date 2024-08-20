from .testcase import LabelTestCase
from task_manager.labels.models import Label


class TestLabelModel(LabelTestCase):
    def test_label_model(self):
        test_label = self.test_labels['create']['valid']
        label = Label.objects.create(**test_label)

        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertEqual(label.name, test_label['name'])
