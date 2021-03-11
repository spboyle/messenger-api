from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=999)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages')
    created = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=999999)
