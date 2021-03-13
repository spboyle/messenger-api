from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse
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
        queryset = self.get_queryset()
        messages = [MessageList.serialize(message) for message in queryset]
        response = {
            'data': messages,
            'count': len(messages)
        }
        return JsonResponse(response, status=200)

    def get_queryset(self):
        return self.model.objects.order_by('-created')
