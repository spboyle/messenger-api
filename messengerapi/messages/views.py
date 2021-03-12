from django.core import serializers
from django.http import JsonResponse
from django.views.generic import ListView

from messengerapi.messages.models import Message


class MessageList(ListView):
    model = Message

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        messages = serializers.serialize('json', queryset)
        response = {
            'data': messages,
            'count': len(messages)
        }
        return JsonResponse(response, status=200)
