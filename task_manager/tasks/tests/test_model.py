from .testcase import TaskTestCase
from task_manager.tasks.models import Task


class TestTaskInstanceCreate(TaskTestCase):
    """Test Task Model"""

    def test_create_instance(self):
        """
        Test create Task object with proper credentials
        Assert objects count increases by one.
        Assert name, description and author are accurate.
        """
        credentials = self.test_task['create']['valid'].copy()
        task = Task.objects.create(
            name=credentials['name'],
            description=credentials['description'],
            author=self.user,
            status=self.status
        )

        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(task.name, credentials['name'])
        self.assertEqual(task.description, credentials['description'])
        self.assertEqual(task.author, self.user)
