import datetime
import json

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from django.utils import timezone

from messengerapi.messages.views import MessageList
from messengerapi.messages.factories import MessageFactory
from messengerapi.messages.models import Message
from messengerapi.users.factories import UserFactory


class MessageListPostTestCase(TestCase):
    def test_post_invalid(self):
        """
        Should return a 400 when users do not exist
        """
        sender = UserFactory()
        data = {
            'sender': sender.id,
            'recipient': 999,
            'text': '...'
        }

        response = self.client.post(
            reverse('messages:list'),
            content_type='application/json',
            data=data,
        )
        self.assertEqual(400, response.status_code)

    def test_post_success_creates_message(self):
        """
        Should create a message when all correct parameters are passed in
        """
        sender, recipient = UserFactory(), UserFactory()

        data = {
            'sender': sender.id,
            'recipient': recipient.id,
            'text': 'Hello World!',
        }

        response = self.client.post(
            reverse('messages:list'),
            content_type='application/json',
            data=data,
        )
        actual_message = Message.objects.get()
        self.assertEqual(sender.id, actual_message.sender.id)
        self.assertEqual(recipient.id, actual_message.recipient.id)
        self.assertEqual(data['text'], actual_message.text)

    def test_post_success_response(self):
        """
        Should return 201 and message data when successfully creating message
        """
        sender, recipient = UserFactory(), UserFactory()

        data = {
            'sender': sender.id,
            'recipient': recipient.id,
            'text': 'Hello World!',
        }

        response = self.client.post(
            reverse('messages:list'),
            content_type='application/json',
            data=data,
        )
        actual_data = json.loads(response.content)

        self.assertEqual(201, response.status_code)
        self.assertEqual(data['sender'], actual_data['sender'])
        self.assertEqual(data['recipient'], actual_data['recipient'])
        self.assertEqual(data['text'], actual_data['text'])
