from django.urls import include, path


urlpatterns = [
    path('messages/', include('messengerapi.messages.urls')),
    path('users/', include('messengerapi.users.urls')),
]
