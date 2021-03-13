import datetime

from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.generic import ListView

from messengerapi.messages.models import Message


class MessageList(ListView):
    model = Message

    @staticmethod
    def serialize(message):
        serialized_message = model_to_dict(message)
        serialized_message.update({
            'sender': message.sender.name,
            'recipient': message.recipient.name
        })
        return serialized_message

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
        return self.model.objects.filter(
            created__gt=self.from_date
        ).order_by('-created')[:self.limit]

    # Query params
    @property
    def from_date(self):
        query_param = self.request.GET.get('fromDate')
        if query_param:
            try:
                return datetime.datetime.fromtimestamp(int(query_param), timezone.utc)
            except (ValueError, OverflowError):
                raise ValidationError(f'Unacceptable UTC timestamp: {query_param}')

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
