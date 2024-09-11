from .testcase import TaskTestCase
from task_manager.tasks.forms import TaskForm


class TestTaskForm(TaskTestCase):
    """Test Task form"""

    def test_task_form_valid(self):
        """
        Assert form with valid credentials is valid
        """

        credentials = self.test_task['create']['valid'].copy()
        form = TaskForm(data=credentials)

        self.assertTrue(form.is_valid())

    def test_task_form_missing_field(self):
        """
        Assert form with missing field is not valid
        """

        credentials = self.test_task['create']['missing_field'].copy()
        form = TaskForm(data=credentials)

        self.assertFalse(form.is_valid())
