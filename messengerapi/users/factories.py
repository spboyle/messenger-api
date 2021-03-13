import factory.faker, factory.django

from messengerapi.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    name = factory.Faker('name')
    email = factory.Faker('email')
