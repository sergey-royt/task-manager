from .testcase import TaskTestCase
from task_manager.tasks.models import Task


class TestTaskInstanceCreate(TaskTestCase):
    def test_create_instance(self):
        credentials = self.test_task['create']['valid'].copy()
        task = Task.objects.create(**credentials)
        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(task.name, credentials['name'])
        self.assertEqual(task.description, credentials['description'])
        self.assertEqual(task.author, self.user)
