from .testcase import TaskTestCase
from task_manager.tasks.forms import TaskForm


class TestTaskForm(TaskTestCase):
    def test_task_form_valid(self):
        credentials = self.test_task['create']['valid'].copy()
        form = TaskForm(data=credentials)

        self.assertTrue(form.is_valid())

    def test_task_form_missing_field(self):
        credentials = self.test_task['create']['missing_field'].copy()
        form = TaskForm(data=credentials)

        self.assertFalse(form.is_valid())
