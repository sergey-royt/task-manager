from .testcase import LabelTestCase
from task_manager.labels.forms import LabelForm


class TestLabelForm(LabelTestCase):
    def test_label_form_valid(self):
        data = self.test_labels['create']['valid'].copy()
        form = LabelForm(data=data)

        self.assertTrue(form.is_valid())

    def test_label_form_missing_field(self):
        data = self.test_labels['create']['missing_field'].copy()
        form = LabelForm(data=data)

        self.assertFalse(form.is_valid())

    def test_label_form_exists(self):
        data = self.test_labels['create']['exists'].copy()
        form = LabelForm(data=data)

        self.assertFalse(form.is_valid())
