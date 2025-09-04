from rest_framework import viewsets, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.conf import settings
from .models import Chat, ChatInvite
from django.http import HttpResponseBadRequest
class SendInviteView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # keep API protected 
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail":"email required"}, status=400)

        # (A) ensure a chat exists between inviter and (future) recipient user record (if any)
        recipient = User.objects.filter(email=email).first()
        if recipient:
            # order users to avoid duplicates
            u1, u2 = sorted([request.user.id, recipient.id])
            chat, _ = Chat.objects.get_or_create(user1_id=u1, user2_id=u2)
        else:
            chat = None

        invite = ChatInvite.objects.create(inviter=request.user, email=email, chat=chat)
        url = request.build_absolute_uri(reverse("magic-login", args=[invite.token]))

        send_mail(
            subject="Join my lab chat",
            message=f"Click to join the chat: {url}\nThis link expires in 2 hours.",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"ok": True})

from django.views import View

class MagicLoginView(View):
    def get(self, request, token):
        invite = get_object_or_404(ChatInvite, token=token, used=False)
        if invite.is_expired:
            return Response("Link expired. Ask your friend to send a new invite.")

        # Get or create the recipient user
        user, _ = User.objects.get_or_create(
            email=invite.email,
            defaults={"username": invite.email.split("@")[0] + "_" + invite.token[:5]}
        )

        # Ensure a chat exists between inviter and recipient
        u1, u2 = sorted([invite.inviter.id, user.id])
        chat, _ = Chat.objects.get_or_create(user1_id=u1, user2_id=u2)

        # mark invite used
        invite.chat = chat
        invite.used = True
        invite.save()

        # log the user in (session auth)
        login(request, user)

        # redirect to your minimal frontend with the chat id prefilled
        return redirect(f"/?chat_id={chat.id}")
