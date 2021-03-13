from django.utils import timezone
import factory, factory.django
from faker import Faker

from messengerapi.messages.models import Message
from messengerapi.users.factories import UserFactory


fake = Faker()


def make_date(message):
    if message.recent:
        return fake.date_time_between('-30d', 'now', tzinfo=timezone.utc)
    else:
        return fake.date_time_between('-1yr', '-31d', tzinfo=timezone.utc)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    class Params:
        recent = True

    sender = factory.SubFactory(UserFactory)
    recipient = factory.SubFactory(UserFactory)
    created = factory.LazyAttribute(make_date)
