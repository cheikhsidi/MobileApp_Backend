from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer
from .consumers import ChatConsumer
# from .views import MyThreads

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    # re_path(r'^ws/thread/(?P<room_name>[^/]+)/$', ThreadConsumer),
    # re_path(r'^ws/chat/image/(?P<room_name>[^/]+)/$', ChatImageConsumer),
]


# from channels.generic.websockets import WebsocketDemultiplexer
# # from channels.routing import route_class
# from channels.routing import route_class, route

# from chat.bindings import ChatBinding, MessageBinding


# class APIDemultiplexer(WebsocketDemultiplexer):

#     mapping = {
#       'chats': 'chats_channel',
#       'messages': 'messages_channel'
#     }

# channel_routing = [
#     route_class(APIDemultiplexer),
#     route("chats_channel", ChatBinding.consumer),
#     route("messages_channel", MessageBinding.consumer)
# ]