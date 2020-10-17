from accounts.models import CustomUser
from rest_framework import serializers
from chat.models import Thread, ChatMessage, ChatImage
from accounts.serializers import UserSerializer
# 
# User Serializer
class ThreadSerializer(serializers.ModelSerializer):
    """For Serializing Thread"""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = Thread
        fields = ['id', 'sender', 'receiver',  'timestamp', 'category', 'item']
# 
# Message Serializer
class ChatSerializer(serializers.ModelSerializer):
    """For Serializing Chat"""
    thread = ThreadSerializer(read_only=True)
    sender = serializers.SlugRelatedField(many=False, slug_field='phone', queryset=CustomUser.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='phone', queryset=CustomUser.objects.all())
    # print('==============================:              ', sender)
    class Meta:
        model = ChatMessage
        fields = ['thread', 'user', 'receiver', 'message', 'timestamp', 'is_read']

# Message Serializer
class ChatImageSerializer(serializers.ModelSerializer):
    """For Serializing Chat"""
    thread = ThreadSerializer(read_only=True)
    user = serializers.SlugRelatedField(many=False, slug_field='phone', queryset=CustomUser.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='phone', queryset=CustomUser.objects.all())
    # print('==============================:              ', sender)
    class Meta:
        model = ChatImage
        fields = ['thread', 'user', 'image', 'timestamp']