from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import ChatViewSet, MessageViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt  # only needed if you choose to exempt

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),                  # exposes /api/chats/, /api/messages/ via the router:contentReference[oaicite:1]{index=1}
    path('api/auth/token/', csrf_exempt(obtain_auth_token)),  # POST username/password -> {"token": "..."}
    path('', include('chat.urls')),                      # serves your minimal frontend at "/"
]
