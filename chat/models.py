from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_initiated")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_received")

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


# chat/models.py
import secrets
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def generate_token():
    # must be a top-level callable with no args so Django can serialize it
    return secrets.token_urlsafe(32)

class ChatInvite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invites_sent")
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True, default=generate_token, editable=False)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, null=True, blank=True, related_name="invites")
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    @property
    def is_expired(self):
        return self.created_at < timezone.now() - datetime.timedelta(hours=2)
