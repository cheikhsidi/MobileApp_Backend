from accounts.models import CustomUser
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.shortcuts import render, get_object_or_404
from .models import ChatMessage, Thread, ChatImage
from django.db.models import Q
from .views import get_last_10_messages, get_user_contact, get_current_chat, get_all_threads
from datetime import datetime
from . import serializers

# ####################################### django rest framework channels Start ################
from . import models
from . import serializers
from djangochannelsrestframework import permissions
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)

# from djangochannelsrestframework.observer.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import ObserverModelInstanceMixin
# from djangochannelsrestframework.observer import model_observer

# @model_observer(models.Thread)
# async def model_activity(self, message, observer=None, **kwargs):
#     # send activity to your frontend
#     await self.send_json(message)


# class ThreadConsumer(CreateModelMixin, GenericAsyncAPIConsumer):
#     queryset = Thread.objects.all()
#     serializer_class = serializers.ThreadSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     # @model_observer(models.Thread)
#     # async def model_activity(self, message, observer=None, **kwargs):
#     # # send activity to your frontend
#     #     await self.send_json(message)

#     def get_queryset(self):
#         """
#         This view should return a list of all the Chats
#         for the currently authenticated user.
#         """
#         user = self.request.user
#         return Thread.objects.filter(Q(sender=user) | Q(receiver=user))

#     def perform_create(self, serializer):
#         print('this is my request data =============', self.request.data)
#         # phone = self.request.data.rceiver

#         receiver = get_object_or_404(CustomUser, phone=self.request.data['receiver'])
#         serializer.save(sender=self.request.user, receiver=receiver)
#         # serializer.save(receiver=receiver)

# class ChatImageConsumer(CreateModelMixin, GenericAsyncAPIConsumer):
#     queryset = ChatImage.objects.all()
#     serializer_class = serializers.ChatImageSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     def get_queryset(self):
#         """
#         This view should return a list of all the Chats
#         for the currently authenticated user.
#         """
#         # user = self.request.user
#         thread = self.request.data['threadId']
#         return ChatImage.objects.filter(threadId = thread)

#     # def perform_create(self, serializer):
#     #     print('this is my request data =============', self.request.data)
#     #     # phone = self.request.data.rceiver
#     #     user = self.request.user
#     #     receiver = get_object_or_404(CustomUser, phone=self.request.data['receiver'])
#     #     serializer.save(sender=self.request.user, receiver=receiver)
#     #     return ChatImage.objects.filter(threadId = thread)
#         # serializer.save(receiver=receiver)

# ####################################### django rest framework channels End ################
class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = get_last_10_messages(data['threadId'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)


    def new_message(self, data):
        print('==========================1', data)
        current_chat = get_current_chat(data['threadId'])
        user =  CustomUser.objects.get(id = data['author'])
        thread = Thread.objects.get(id = data['threadId'])
        # print('============ Current Chat-----', current_chat.sender)
        message = ChatMessage.objects.create(
            user=user,
            message=data['message'],
            thread = thread)
        # current_chat = get_current_chat(data['threadId'])
        # print('============ Current Chat-----', current_chat)
        # current_chat.messages.add(message)
        # current_chat.save()
        print(message)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def new_message_image(self, data):
        print('==========================1', data)
        current_chat = get_current_chat(data['threadId'])
        user =  CustomUser.objects.get(id = data['author'])
        thread = Thread.objects.get(id = data['threadId'])
        # print('============ Current Chat-----', current_chat.sender)
        message = ChatImage.objects.create(
            user=user,
            image=data['image'],
            thread = thread)
        # current_chat = get_current_chat(data['threadId'])
        # print('============ Current Chat-----', current_chat)
        # current_chat.messages.add(message)
        # current_chat.save()
        print(message)
        content = {
            'command': 'new_message_image',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            '_id': message.id,
            'text':message.message,
            'createdAt': str(message.timestamp),
            # 'createdAt':str(datetime.strptime(str(message.timestamp), '%m-%d-%Y %H:%M:%S.%f')),
            'user':{
                '_id':message.user.id,
                'name': message.user.firstName,
            }
            # 'content': message.message,
            # 'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message_image' : new_message_image,
        'new_message': new_message,
        # 'new_thread': new_thread,

    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print('room name========',  self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name
        print('room froup name========',  self.room_group_name)
        # self.user = self.scope["user"]
        print('================== this is the scope', self.scope)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))


# import re
# from typing import Dict, Any

# from channels.consumer import AsyncConsumer
# from django.db.models import QuerySet
# from djangochannelsrestframework.decorators import action

# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import (
#     ListModelMixin,
#     CreateModelMixin,
#     PatchModelMixin,
#     DeleteModelMixin,
#     RetrieveModelMixin
# )
# from djangochannelsrestframework.observer import model_observer
# from djangochannelsrestframework.permissions import IsAuthenticated

# from chat import models, serializers


# # class IsAuthenticatedForWrite(IsAuthenticated):
# #     async def has_permission(
# #             self, scope: Dict[str, Any],
# #             consumer: AsyncConsumer,
# #             action: str,
# #             **kwargs
# #     ) -> bool:
# #         """
# #         This method will permit un-authenticated requests
# #          for non descrutive actions only.
# #         """

# #         if action in ('list', 'retrieve'):
# #             return True
# #         return await super().has_permission(
# #             scope,
# #             consumer,
# #             action,
# #             **kwargs
# #         )


# class LiveChatConsumer(
#     ListModelMixin,
#     RetrieveModelMixin,
#     CreateModelMixin,
#     PatchModelMixin,
#     DeleteModelMixin,
#     GenericAsyncAPIConsumer
# ):
#     queryset = models.ChatMessage.objects.all()
#     serializer_class = serializers.ChatSerializer
#     permission_classes = (IsAuthenticated,)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.subscribed_to_list = False
#         # self.subscribed_to_hashtag = None

#     def filter_queryset(self, queryset: QuerySet, **kwargs):
#         queryset = super().filter_queryset(queryset=queryset, **kwargs)

#         # we need to ensure that only the author can edit there chats.
#         if kwargs.get('action') == 'list':
#             filter = kwargs.get("body_contains", None)
#             if filter:
#                 queryset = queryset.filter(body__icontains=filter)
#             # users can list the latest 500 chats
#             return queryset.order_by('-created_at')[:500]

#         if kwargs.get('action') == 'retrieve':
#             return queryset

#         # for other actions we can only expose the chats created by this user.
#         return queryset.filter(author=self.scope.get("user"))

#     @model_observer(models.ChatMessage)
#     async def chat_change_handler(self, message, observer=None, **kwargs):
#         # called when a subscribed item changes
#         await self.send_json(message)

#     @chat_change_handler.groups_for_signal
#     def chat_change_handler(self, instance: models.ChatMessage, **kwargs):
#         # DO NOT DO DATABASE QURIES HERE
#         # This is called very oftern through the lifecycle of every intance of a ChatMessage model
#         for hashtag in re.findall(r"#[a-z0-9]+", instance.body.lower()):
#             yield f'-hashtag-{hashtag}'
#         yield '-all'

#     # @chat_change_handler.groups_for_consumer
#     # def chat_change_handler(self, hashtag=None, list=False, **kwargs):
#     #     # This is called when you subscribe/unsubscribe
#     #     if hashtag is not None:
#     #         yield f'-hashtag-#{hashtag}'
#     #     if list:
#     #         yield '-all'

#     # @action()
#     # async def subscribe_to_hashtag(self, hashtag, **kwargs):
#     #     await self.clear_subscription()
#     #     await self.chat_change_handler.subscribe(hashtag=hashtag)
#     #     self.subscribed_to_hashtag = hashtag
#     #     return {}, 201

#     # @action()
#     # async def subscribe_to_list(self, **kwargs):
#     #     await self.clear_subscription()
#     #     await self.chat_change_handler.subscribe(list=True)
#     #     self.subscribed_to_list = True
#     #     return {}, 201

#     # @action()
#     # async def unsubscribe_from_hashtag(self, hashtag, **kwargs):
#     #     await self.chat_change_handler.unsubscribe(hashtag=hashtag)
#     #     if self.subscribe_to_hashtag == hashtag:
#     #         self.subscribed_to_hashtag = None
#     #     return {}, 204

#     # @action()
#     # async def unsubscribe_from_list(self, **kwargs):
#     #     await self.chat_change_handler.unsubscribe(list=True)
#     #     self.subscribed_to_list = False
#     #     return {}, 204

#     # async def clear_subscription(self):
#     #     if self.subscribe_to_hashtag is not None:
#     #         await self.chat_change_handler.unsubscribe(
#     #             hashtag=self.subscribe_to_hashtag
#     #         )
#     #         self.subscribed_to_hashtag = None

#     #     if self.subscribe_to_list:
#     #         await self.chat_change_handler.unsubscribe(
#     #             list=True
#     #         )
#     #         self.subscribed_to_list = False

#     @chat_change_handler.serializer
#     def chat_change_handler(self, instance: models.ChatMessage, action, **kwargs):
#         if action == 'delete':
#             return {"pk": instance.pk}
#         return {"pk": instance.pk, "data": {"body": instance.body}}