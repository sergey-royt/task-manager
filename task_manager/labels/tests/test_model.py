from .testcase import LabelTestCase
from task_manager.labels.models import Label


class TestLabelModel(LabelTestCase):
    """Test Label model"""

    def test_label_model(self) -> None:
        """
        Test create Label object with valid credentials
        Assert object count increase by one
        Assert object name is accurate
        """

        test_label = self.test_labels['create']['valid']
        label = Label.objects.create(**test_label)

        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertEqual(label.name, test_label['name'])
