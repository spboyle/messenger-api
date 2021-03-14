import datetime
import json

from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode
from django.utils import timezone

from messengerapi.messages.views import MessageList
from messengerapi.messages.factories import MessageFactory
from messengerapi.users.factories import UserFactory
from messengerapi.users.models import User
from messengerapi.settings import ISO_FORMAT


class MessageListGetTestCase(TestCase):
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
        sender = actual_as_json['sender']
        recipient = actual_as_json['recipient']
        self.assertEqual(expected_obj.sender.name, sender['name'])
        self.assertEqual(expected_obj.sender.email, sender['email'])
        self.assertEqual(expected_obj.sender.id, sender['id'])
        self.assertEqual(expected_obj.recipient.name, recipient['name'])
        self.assertEqual(expected_obj.recipient.email, recipient['email'])
        self.assertEqual(expected_obj.recipient.id, recipient['id'])
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
            self.assertEqual(expected_obj.sender.name, actual_as_json['sender']['name'])
            self.assertEqual(expected_obj.recipient.name, actual_as_json['recipient']['name'])

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
        self.assertEqual(recent_message.sender.name, actual_as_json['sender']['name'])
        self.assertEqual(recent_message.recipient.name, actual_as_json['recipient']['name'])

    def test_get_from_date_query_param_present(self):
        """
        Should filter by the fromDate query param when present
        """
        from_date = timezone.now() - datetime.timedelta(days=15)
        old_message = MessageFactory(created=from_date - datetime.timedelta(days=1))
        recent_message = MessageFactory(created=from_date + datetime.timedelta(days=1))

        # Manually convert to isoformat python datetime.isoformat() returns with offset and/or
        # decimals in the seconds place
        query_params = urlencode({'fromDate': from_date.strftime(ISO_FORMAT)})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)
        actual_data = json.loads(response.content)

        self.assertEqual(1, len(actual_data['data']))
        self.assertEqual(1, actual_data['count'])

        actual_as_json = actual_data['data'][0]
        self.assertEqual(recent_message.sender.name, actual_as_json['sender']['name'])
        self.assertEqual(recent_message.recipient.name, actual_as_json['recipient']['name'])

    def test_get_from_date_query_param_invalid(self):
        """
        Should return 400 when query param for fromDate is invalid
        """
        query_params = urlencode({'fromDate': '2005-12-25'})

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

    def test_get_sender_query_param_present(self):
        """
        Should filter by the sender query param when present
        """
        expected_sender = MessageFactory.create_batch(3)[0].sender
        query_params = urlencode({'senderId': expected_sender.id})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)
        actual_data = json.loads(response.content)

        self.assertEqual(1, len(actual_data['data']))
        self.assertEqual(1, actual_data['count'])

        actual_sender = actual_data['data'][0]['sender']
        self.assertEqual(expected_sender.email, actual_sender['email'])
        self.assertEqual(expected_sender.name, actual_sender['name'])

    def test_get_recipient_query_param_present(self):
        """
        Should filter by the recipient query param when present
        """
        expected_recipient = MessageFactory.create_batch(3)[0].recipient
        query_params = urlencode({'recipientId': expected_recipient.id})

        url = '{}?{}'.format(reverse('messages:list'), query_params)
        response = self.client.get(url)
        actual_data = json.loads(response.content)

        self.assertEqual(1, len(actual_data['data']))
        self.assertEqual(1, actual_data['count'])

        actual_recipient = actual_data['data'][0]['recipient']
        self.assertEqual(expected_recipient.email, actual_recipient['email'])
        self.assertEqual(expected_recipient.name, actual_recipient['name'])
