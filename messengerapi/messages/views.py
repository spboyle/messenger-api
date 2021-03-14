import datetime
import json

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.generic import ListView

from messengerapi.messages.models import Message
from messengerapi.users.models import User
from django.conf import settings


class MessageList(ListView):
    model = Message

    ################################
    # POST /messages/
    ################################
    def post(self, request, *args, **kwargs):
        try:
            message = Message.objects.create(**self.post_data)
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)

        return JsonResponse(self.serialize(message), status=201)

    ################################
    # GET /messages/
    ################################
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except ValidationError as e:
            return JsonResponse({'error': e.message}, status=400)

        messages = [MessageList.serialize(message) for message in queryset]
        response = {
            'data': messages,
            'count': len(messages)
        }
        return JsonResponse(response, status=200)

    def get_queryset(self):
        return self.model.objects.filter(**self.query_params).order_by('-created')[:self.limit]

    @staticmethod
    def serialize(message):
        serialized_message = model_to_dict(message)
        serialized_message.update({
            'sender': model_to_dict(message.sender),
            'recipient': model_to_dict(message.recipient),
        })
        return serialized_message

    ################################
    # Query params
    ################################
    @property
    def query_params(self):
        if not hasattr(self, '_query_params'):
            self._query_params = {'created__gt': self.from_date}

            if 'senderId' in self.request.GET:
                self._query_params['sender__id'] = self.request.GET['senderId']
            if 'recipientId' in self.request.GET:
                self._query_params['recipient__id'] = self.request.GET['recipientId']

        return self._query_params

    @property
    def from_date(self):
        query_param = self.request.GET.get('fromDate')
        if query_param:
            try:
                my_value = timezone.make_aware(datetime.datetime.strptime(query_param, settings.ISO_FORMAT))
                return my_value
            except (ValueError, OverflowError):
                raise ValidationError(f'Unacceptable ISO format: {query_param}')

        return timezone.now() - datetime.timedelta(days=30)

    @property
    def limit(self):
        try:
            query_param = int(self.request.GET.get('limit', 100))
        except ValueError:
            raise ValidationError(f'Unacceptable limit: {query_param}')

        if query_param < 1 or query_param > 9999:
            raise ValidationError(f'Limit outside of bounds [1, 9999]: {query_param}')

        return query_param

    ################################
    # Post Data
    ################################
    @property
    def post_data(self):
        post_data = json.loads(self.request.body)
        MessageList.check_user(post_data.get('senderId'))
        MessageList.check_user(post_data.get('recipientId'))
        post_data['sender_id'] = post_data.pop('senderId')
        post_data['recipient_id'] = post_data.pop('recipientId')
        return post_data

    @staticmethod
    def check_user(user_id):
        try:
            User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise ValidationError(f'User {user_id} not found')
