import factory


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "statuses.Status"

    name = factory.Faker("word")
