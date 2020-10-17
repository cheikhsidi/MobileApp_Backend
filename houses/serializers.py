from .models import House, Rating, Reservation
from accounts.serializers import UserSerializer
from rest_framework.fields import ImageField
from django.db.models import Avg
# from accounts.models import CustomUser
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    customerId = serializers.ReadOnlyField(source='customerId.phone')
    rates = serializers.PrimaryKeyRelatedField(many=True, read_only=True, default=5)
    class Meta:
        model = House
        fields = ('id', 'customerId', 'latitude', 'longitude', 'city', 'area', 
                    'subArea', 'category', 'bedrooms', 
                    'salons', 'bathrooms', 'other_rooms', 
                    'description', 'cost', 'image1', 'image2','image3', 'image4', 'image5', 'rates')
        
        # fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category']
        return data


class RateListingField(serializers.RelatedField):
    def to_representation(self, value):
        Avgerage_rate = Avg(value.rate)
        return Avgerage_rate


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'review']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['rate', 'review']
    #     return data

class HouseSerializerDetail(serializers.ModelSerializer):
    customerId = UserSerializer(read_only=True)
    # rates = serializers.PrimaryKeyRelatedField(many=True, queryset=Rating.objects.all())
    # rates = RateListingField(read_only=True)
    rates = RatingSerializer(many=True, read_only=True)
    # rates = RatingSerializer(read_only=True, many=True)
    class Meta:
        model = House
        fields = ('id','location', 'city', 'area', 
                    'subArea', 'category', 'bedrooms', 
                    'salons', 'bathrooms', 'other_rooms', 
                    'description', 'cost', 'image1', 'image2','image3', 'image4', 'image5', 'rates', 'customerId')
        # depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category']
        return data


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        # customerId = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
        fields = '__all__'


