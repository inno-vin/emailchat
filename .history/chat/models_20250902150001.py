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
