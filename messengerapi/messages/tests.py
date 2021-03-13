from datetime import datetime
import json

from django.test import TestCase
from django.urls import reverse

from messengerapi.messages.views import MessageList
from messengerapi.messages.factories import MessageFactory
from messengerapi.users.factories import UserFactory


class MessageListTestCase(TestCase):
    def test_get_empty(self):
        """
        Should return empty data with count=0 When no messages are present
        """
        response = self.client.get(reverse('messages:list'))
        actual_data = json.loads(response.content)
        expected_data = {'data': [], 'count': 0}
        self.assertEqual(expected_data, actual_data)

    def test_get_one(self):
        """
        Should return all appropriate attributes for one message
        """
        expected_obj = MessageFactory()
        response = self.client.get(reverse('messages:list'))
        actual_data = json.loads(response.content)

        self.assertEqual(1, actual_data['count'])
        self.assertEqual(1, len(actual_data['data']))

        actual_as_json = actual_data['data'][0]
        self.assertEqual(expected_obj.sender.name, actual_as_json['sender'])
        self.assertEqual(expected_obj.recipient.name, actual_as_json['recipient'])
        expected_time = expected_obj.created.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.assertEqual(expected_time, actual_as_json['created'])

    def test_get_multiple(self):
        """
        Should return all messages, sorted by descending
        """
        expected_data_as_objects = sorted(
            [MessageFactory() for i in range(3)],
            key=lambda message: message.created,
            reverse=True
        )
        response = self.client.get(reverse('messages:list'))
        actual_data = json.loads(response.content)

        print(actual_data)
        self.assertEqual(3, len(actual_data['data']))
        self.assertEqual(3, actual_data['count'])

        for expected_obj, actual_as_json in zip(expected_data_as_objects, actual_data['data']):
            self.assertEqual(expected_obj.sender.name, actual_as_json['sender'])
            self.assertEqual(expected_obj.recipient.name, actual_as_json['recipient'])
