from django.urls import include, re_path


urlpatterns = [
    re_path('messages/?', include('messengerapi.messages.urls')),
    re_path('users/?', include('messengerapi.users.urls')),
]
