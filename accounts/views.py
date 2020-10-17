from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.http import Http404
# from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
# from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)



from django.views.generic import View
# from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail

from .models import  CustomUser
from accounts.serializers import CreateUserSerializer, LoginSerializer, UserSerializer, UpdateSerializer, ChangePasswordSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer
import time



import logging
from django.core.cache import cache
logger = logging.getLogger(__name__)
import arrow
# class TimeDelayMixin(object, ):

#     def dispatch(self, request, *args, **kwargs):
#         time.sleep(3)
#         return super().dispatch(request, *args, **kwargs)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

# Register Class
class CreateUserAPIView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        firstName = request.data.get('firstName', False)
        lastName = request.data.get('lastName', False)
        email = request.data.get('email', False)
        try:
            phone = int(phone)
        except:
            return Response({
                'error':'Phone must be digits'
            }, status=HTTP_400_BAD_REQUEST)

        if phone and password and firstName and lastName and email:
            old = CustomUser.objects.filter(phone__iexact=phone)
            if old.exists():
                return Response({'error': 'The phoen you entered is already used please try again or login'},
                            status=HTTP_400_BAD_REQUEST)
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                return Response({
                    "user": UserSerializer(user, context= self.get_serializer_context()).data,
                    "token":AuthToken.objects.create(user)[1]
                })

        else:
            return Response({
                'error':'Please fill outall the fields'
            }, status=HTTP_400_BAD_REQUEST)

# Loggin Attempt
class InvalidLoginAttemptsCache(object):
    @staticmethod
    def _key(phone):
        return 'invalid_login_attempt_{}'.format(phone)

    @staticmethod
    def _value(lockout_timestamp, timebucket):
        return {
            'lockout_start': lockout_timestamp,
            'invalid_attempt_timestamps': timebucket
        }

    @staticmethod
    def delete(phone):
        try:
            cache.delete(InvalidLoginAttemptsCache._key(phone))
        except Exception as e:
            logger.exception(e.message)

    @staticmethod
    def set(phone, timebucket, lockout_timestamp=None):
        try:
            key = InvalidLoginAttemptsCache._key(phone)
            value = InvalidLoginAttemptsCache._value(lockout_timestamp, timebucket)
            cache.set(key, value)
        except Exception as e:
            logger.exception(e.message)

    @staticmethod
    def get(phone):
        try:
            key = InvalidLoginAttemptsCache._key(phone)
            return cache.get(key)
        except Exception as e:
            logger.exception(e.message)

# Logging CLass
class LoginAPIView( generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # get the email from the form or POST data
        phone = request.data.get("phone")
        password = request.data.get("password")

        user = authenticate(phone=phone, password=password)
        if not user:
            
            locked_out = False
            cache_results = InvalidLoginAttemptsCache.get(phone)
            lockout_timestamp = None
            now = arrow.utcnow()
            invalid_attempt_timestamps = cache_results['invalid_attempt_timestamps'] if cache_results else []

            # clear any invalid login attempts from the timestamp bucket that were longer ago than the range 
            invalid_attempt_timestamps = [timestamp for timestamp in invalid_attempt_timestamps if timestamp > now.shift(minutes=-15).timestamp]

            # add this current invalid login attempt to the timestamp bucket
            invalid_attempt_timestamps.append(now.timestamp)
            # check to see if the user has enough invalid login attempts to lock them out
            if len(invalid_attempt_timestamps) >= 3:
                lockout_timestamp = now.timestamp
                # This is also where you'll need to add an error to the form to both prevent their successful authentication and let the user know
            # Add a cache entry. If they've already got one, this will overwrite it, otherwise it's a new one
            InvalidLoginAttemptsCache.set(phone, invalid_attempt_timestamps, lockout_timestamp)
            if cache_results and cache_results.get('lockout_start'):
                lockout_start = arrow.get(cache_results.get('lockout_start'))
                locked_out = lockout_start >= arrow.utcnow().shift(minutes=-15)
                if not locked_out:
                    InvalidLoginAttemptsCache.delete(phone)
                else:
                    return Response({
                        'error':'You account is loacked out'
                    }, status=HTTP_400_BAD_REQUEST)
            # try:
            #     phone = int(phone)
            # except:
            #     return Response({
            #         'error':'Phone must be digits'
            #     }, status=HTTP_400_BAD_REQUEST)       
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
                # Add an error to the form to let the user know they're locked out and can't log in. Code to do this will vary depending on whether you're in a view or the form class itself
        else:
            # If they don't have an entry in the cache, we know they're not locked out, and we can process their request


            
            # user_data = CustomUser.objects.all().filter(phone=phone)
            # try:
            #     phone = int(phone)
            # except:
            #     return Response({
            #         'error':'Phone must be digits'
            #     }, status=HTTP_400_BAD_REQUEST)
            # if phone is None or password is None:
            #     return Response({'error': 'Please provide both phone and password'},
            #                     status=HTTP_400_BAD_REQUEST)
           
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            return Response({
                "user": UserSerializer(user, context= self.get_serializer_context()).data,
                "token":AuthToken.objects.create(user)[1]
            })
        # login(request, user)
        # return super().post(request, format=None)



# Logout API view
class LogoutUserAPIView(APIView):
    # queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)

# User Profile
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        try:
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data)
        # user = self.get_object(pk)
        # serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# Chnage Password
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(
            #     request=request).domain

            current_site = 'localhost:8000'
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            email_body = f'Hello,{user.firstName} \n Use link below to reset your password  \n' + absurl + f'\n ID   : {uidb64}' + f'\n Verification Code   : {token}'
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)





