from django.core import serializers
from django.http import JsonResponse
from django.views.generic import ListView

from messengerapi.users.models import User


class UserList(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        users = serializers.serialize('json', queryset)
        response = {
            'data': users,
            'count': len(users)
        }

        return JsonResponse(response, status=200)
