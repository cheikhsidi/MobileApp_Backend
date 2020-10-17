from django.db import models
# from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from houses.choices import *


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone')
        if not password:
            raise ValueError('user must have password')
        user = self.model(
            phone = phone
        )
      
        user.set_password(password)
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, phone, password=None):
        user=self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True
            )
        return user
    
class CustomUser(AbstractBaseUser):
    username = None
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    phone = models.IntegerField(unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, blank=True, null = True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=True)
    # title = models.CharField(max_length= 50)
    image =  models.ImageField('uploaded images', default= '/images/ProfileDefault.jpg', blank=True, null=True)

    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
            
    objects = UserManager()

    def __str__(self):
        return str(self.phone) or ''

    def get_full_name(self):
        if self.firstName and self.lastName:
            return self.firstName + self.lastName
        else:
            return self.email

    def get_short_name(self):
        return self.firstName

    def has_perm(self, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active




# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )