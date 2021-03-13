import datetime
import json

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from django.utils import timezone

from messengerapi.messages.views import MessageList
from messengerapi.messages.factories import MessageFactory
from messengerapi.users.factories import UserFactory


class MessageListTestCase(TestCase):
    def test_get_empty(self):
        """
        Should return empty data with count=0 when no messages are present
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
        expected_time = expected_obj.created.strftime('%Y-%m-%dT%H:%M:%SZ')
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

        self.assertEqual(3, len(actual_data['data']))
        self.assertEqual(3, actual_data['count'])

        for expected_obj, actual_as_json in zip(expected_data_as_objects, actual_data['data']):
            self.assertEqual(expected_obj.sender.name, actual_as_json['sender'])
            self.assertEqual(expected_obj.recipient.name, actual_as_json['recipient'])

    def test_get_from_date_query_param_default(self):
        """
        Should only fetch messages in the past 30 days when fromDate query param is absent
        """
        old_message = MessageFactory(recent=False)
        recent_message = MessageFactory(recent=True)
        response = self.client.get(reverse('messages:list'))
        actual_data = json.loads(response.content)

        self.assertEqual(1, len(actual_data['data']))
        self.assertEqual(1, actual_data['count'])

        actual_as_json = actual_data['data'][0]
        self.assertEqual(recent_message.sender.name, actual_as_json['sender'])
        self.assertEqual(recent_message.recipient.name, actual_as_json['recipient'])

    def test_get_from_date_query_param_present(self):
        """
        Should filter by the fromDate query param when present
        """
        from_date = timezone.now() - datetime.timedelta(days=15)
        old_message = MessageFactory(created=from_date - datetime.timedelta(days=1))
        recent_message = MessageFactory(created=from_date + datetime.timedelta(days=1))

        # Convert to int because python datetime.timestamp() method is floating point
        query_params = urlencode({'fromDate': int(from_date.timestamp())})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)
        actual_data = json.loads(response.content)

        self.assertEqual(1, len(actual_data['data']))
        self.assertEqual(1, actual_data['count'])

        actual_as_json = actual_data['data'][0]
        self.assertEqual(recent_message.sender.name, actual_as_json['sender'])
        self.assertEqual(recent_message.recipient.name, actual_as_json['recipient'])

    def test_get_from_date_query_param_invalid(self):
        """
        Should return 400 when query param for fromDate is invalid
        """
        # Convert to int because python datetime.timestamp() method is floating point
        query_params = urlencode({'fromDate': 12345676543512413123})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)

        self.assertEqual(400, response.status_code)

    def test_get_limit_query_param_default(self):
        """
        Should only fetch 100 messages when limit query param is absent
        """
        MessageFactory.create_batch(150)
        response = self.client.get(reverse('messages:list'))
        actual_data = json.loads(response.content)

        self.assertEqual(100, len(actual_data['data']))
        self.assertEqual(100, actual_data['count'])

    def test_get_limit_query_param_present(self):
        """
        Should filter by the limit query param when present
        """
        MessageFactory.create_batch(3)
        query_params = urlencode({'limit': 2})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)
        actual_data = json.loads(response.content)

        self.assertEqual(2, len(actual_data['data']))
        self.assertEqual(2, actual_data['count'])

    def test_get_limit_query_param_invalid(self):
        """
        Should return 400 when query param for limit is invalid
        """
        query_params = urlencode({'limit': -4})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)

        self.assertEqual(400, response.status_code)
