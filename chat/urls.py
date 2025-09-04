from django.urls import path
from django.views.generic import TemplateView
from .views import SendInviteView, MagicLoginView

urlpatterns = [
    path("", TemplateView.as_view(template_name="chat.html"), name="chat-home"),
    path("api/invite/", SendInviteView.as_view(), name="send-invite"),
    path("auth/magic/<str:token>/", MagicLoginView.as_view(), name="magic-login"),
]
