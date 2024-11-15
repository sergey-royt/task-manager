import factory

from task_manager.statuses.tests.factories.status_factory import StatusFactory
from task_manager.users.tests.factories.user_factory import UserFactory


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "tasks.Task"

    name = factory.Faker("name", unique=True)
    status = factory.SubFactory(StatusFactory)
    author = factory.SubFactory(UserFactory)
    executor = factory.SubFactory(UserFactory)
