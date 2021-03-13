from django.urls import path
from messengerapi.messages.views import MessageList


app_name = 'messages'
urlpatterns = [
    path('', MessageList.as_view(), name='list'),
]
