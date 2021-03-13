import json

from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView

from messengerapi.users.models import User


class UserList(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        users = [model_to_dict(user) for user in queryset]
        response = {
            'data': users,
            'count': len(users)
        }
        return JsonResponse(response, status=200)

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create(**json.loads(request.body))
        except IntegrityError:
            return JsonResponse({'error': 'Email is taken'}, status=400)

        return JsonResponse(model_to_dict(user), status=201)
