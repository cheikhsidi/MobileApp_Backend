from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.fields import CurrentUserDefault
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import *
from houses.models import House


class CreateUserSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})


    class Meta:
        model = CustomUser
        fields = ('id', 'phone', 'password', 'email', 'firstName', 'lastName', 'image',)
        extra_kwargs = { 'password':{ 'write_only': True}, 'password2':{ 'write_only': True}}
        # write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active',)

    def create(self, validated_data):
        # user = CustomUser.objects.create_user(validated_data['phone'],
        # validated_data['password'])
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

    

class UserSerializer(serializers.ModelSerializer):
    # houses = serializers.PrimaryKeyRelatedField(many=True, queryset=House.objects.all())
    class Meta:
        model = CustomUser
        fields = ['id', 'firstName', 'lastName', 'phone', 'email', 'image']


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'firstName', 'lastName', 'phone', 'email', 'image']

    def update(self, instance, validated_data):
        # print 'this - here'
        user = CustomUser.objects.get(pk=instance.id)
        user.objects.filter(pk=instance.id)\
                           .update(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=3, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The ID and Code are invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The ID and Code are invalid', 401)
        return super().validate(attrs)
