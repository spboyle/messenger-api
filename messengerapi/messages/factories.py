import factory, factory.django

from messengerapi.messages.models import Message
from messengerapi.users.factories import UserFactory


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    sender = factory.SubFactory(UserFactory)
    recipient = factory.SubFactory(UserFactory)
