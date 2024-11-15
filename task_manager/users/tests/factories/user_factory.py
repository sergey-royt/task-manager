import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.CustomUser"

    password = factory.django.Password("f4K3_Pa$$w0rd")
    username = factory.Faker("user_name", unique=True)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
