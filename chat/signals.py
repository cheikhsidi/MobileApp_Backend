from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Thread



@receiver(post_save)
def post_save(sender, instance, created, **kwargs):
    # print('instance======', instance.item)
    return instance