from .testcase import LabelTestCase
from task_manager.labels.forms import LabelForm


class TestLabelForm(LabelTestCase):
    """Test Label form"""
    def test_label_form_valid(self) -> None:
        """
        Assert form with valid credentials is valid
        """

        data = self.test_labels['create']['valid'].copy()
        form = LabelForm(data=data)

        self.assertTrue(form.is_valid())

    def test_label_form_missing_field(self) -> None:
        """
        Assert form with missing field is not valid
        """

        data = self.test_labels['create']['missing_field'].copy()
        form = LabelForm(data=data)

        self.assertFalse(form.is_valid())

    def test_label_form_exists(self) -> None:
        """
        Assert form with existed name is not valid
        """

        data = self.test_labels['create']['exists'].copy()
        form = LabelForm(data=data)

        self.assertFalse(form.is_valid())
