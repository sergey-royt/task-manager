import factory


class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "labels.Label"

    name = factory.Faker("word")
