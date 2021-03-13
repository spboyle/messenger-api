from django.urls import path
from messengerapi.users.views import UserList

app_name = 'users'
urlpatterns = [
    path('', UserList.as_view(), name='list'),
]
