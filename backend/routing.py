from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
import chat.routing
from .channelsmiddleware import TokenAuthMiddleware



application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            # url(r"^ws/?$", consumers.LiveChatConsumer),
            chat.routing.websocket_urlpatterns
        )
    )
})

