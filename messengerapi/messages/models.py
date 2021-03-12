from django.db import models
from django.utils import timezone

from messengerapi.users.models import User


TEXT_MESSAGE_MAX = 160

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages')
    created = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=TEXT_MESSAGE_MAX)
