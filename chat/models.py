
from django.db import models

from accounts.models import CustomUser
from django.db import models
from django.db.models import Q
# from model_utils import FieldTracker
# from asgiref.sync import async_to_sync



class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_phone): # get_or_create
        phone = user.phone
        if phone == other_phone:
            return None
        qlookup1 = Q(first__phone=phone) & Q(second__phone=other_phone)
        qlookup2 = Q(first__phone=other_phone) & Q(second__phone=phone)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(phone=other_phone)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    sender        = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_thread_sender')
    receiver       = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_thread_receiver')
    timestamp    = models.DateTimeField(auto_now_add=True)
    category     = models.CharField(max_length=50)
    item         = models.IntegerField()
    
    objects      = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user        = models.ForeignKey(CustomUser, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)


class ChatImage(models.Model):
    thread      = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user        = models.ForeignKey(CustomUser, verbose_name='sender', on_delete=models.CASCADE)
    # chat     = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    image      = models.ImageField('uploaded images', blank=True, null=True)