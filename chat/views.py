
from accounts.models import CustomUser
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import ChatMessage, Thread
from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
# from .views import get_user_contact
from .serializers import ChatSerializer, ThreadSerializer

# from . import models
# from djangochannelsrestframework.observer import model_observer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



def get_last_10_messages(threadId):
    chats = ChatMessage.objects.filter(thread=threadId).order_by('-timestamp')
    return chats
    # return chat.order_by('-timestamp').all()[:10]

def get_all_threads(receiver):
    threads = get_object_or_404(Thread, receiver=receiver)
    return threads
    # chat.messages.order_by('-timestamp').all()[:10]
# def get_Current(receiver):
#     threads = get_object_or_404(Thread, receiver=receiver)
#     return threads

def get_user_contact(phone):
    user = get_object_or_404(CustomUser, phone=phone)
    print ('=========================2', user)
    return user


def get_current_chat(threadId):
    # current_thread = Thread.objects.filter(id=threadId).all()
    # return current_thread
    return get_object_or_404(Thread, id=threadId)


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self): 
        queryset = ChatMessage.objects.all()
        rceiver = self.request.user
        phone = self.request.query_params.get('phone', None)
        if phone is not None:
            user = get_user_contact(phone)
            thread = Thread.objects.filter(Q(sender=user) & Q(rceiver=rceiver))
            messages = ChatMessage.objects.all(thread=thread)
        return messages


class ChatDetailView(RetrieveAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatCreateView(CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatUpdateView(UpdateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )





class MyThreads(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ThreadSerializer
    def get_queryset(self):
        """
        This view should return a list of all the Chats
        for the currently authenticated user.
        """
        user = self.request.user
        return Thread.objects.filter(Q(sender=user) | Q(receiver=user))

    def perform_create(self, serializer):
        print('this is my request data =============', self.request.data)
        # phone = self.request.data.rceiver

        receiver = get_object_or_404(CustomUser, phone=self.request.data['receiver'])
        serializer.save(sender=self.request.user, receiver=receiver)
        # serializer.save(receiver=receiver)
        room_group_name = 'chat_%s' % receiver.id
        print('rooooom        ', room_group_name)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(room_group_name, {"type": "chat_message", 'message': {'command': 'new_message','message':2}})

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import Http404, HttpResponseForbidden
# from django.shortcuts import render
# from django.urls import reverse
# from django.views.generic.edit import FormMixin

# from django.views.generic import DetailView, ListView

# # from .forms import ComposeForm
# from .models import Thread, ChatMessage


# class InboxView(LoginRequiredMixin, ListView):
#     # template_name = 'chat/inbox.html'
#     def get_queryset(self):
#         return Thread.objects.by_user(self.request.user)


# class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
#     # template_name = 'chat/thread.html'
#     # form_class = ComposeForm
#     # success_url = './'

#     def get_queryset(self):
#         return Thread.objects.by_user(self.request.user)

#     def get_object(self):
#         other_phone  = self.kwargs.get("phone")
#         obj, created    = Thread.objects.get_or_new(self.request.user, other_phone)
#         if obj == None:
#             raise Http404
#         return obj

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         thread = self.get_object()
#         user = self.request.user
#         message = form.cleaned_data.get("message")
#         ChatMessage.objects.create(user=user, thread=thread, message=message)
#         return super().form_valid(form)



# class ChatView(LoginRequiredMixin, FormMixin, DetailView):
#     # template_name = 'chat/thread.html'
#     # form_class = ComposeForm
#     # success_url = './'

#     def get_queryset(self):
#         return ChatMessage.objects.by_user(self.request.user)

#     def get_object(self):
#         other_phone  = self.kwargs.get("phone")
#         obj, created    = ChatMessage.objects.get_or_new(self.request.user, other_phone)
#         if obj == None:
#             raise Http404
#         return obj

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     # def form_valid(self, form):
#     #     message = self.get_object()
#     #     user = self.request.user
#     #     message = form.cleaned_data.get("message")
#     #     ChatMessage.objects.create(user=user, thread=thread, message=message)
#     #     return super().form_valid(form)