from django.core import serializers
from django.http import JsonResponse
from django.views.generic import ListView

from messengerapi.messages.models import Message


class MessageList(ListView):
    model = Message

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        messages = serializers.serialize('json', queryset)
        return JsonResponse(messages, status=200, safe=False)
