from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser
from .choices import *


class House(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name = 'houses', on_delete=models.CASCADE)
    # location = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    subArea = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank = True,  null=True)
    bedrooms = models.IntegerField()
    salons = models.IntegerField()
    bathrooms = models.IntegerField()
    other_rooms = models.IntegerField()
    description = models.TextField()
    cost = models.IntegerField()
    image1 = models.ImageField('uploaded images', default= '/images/houseDefault.jpg', blank=True, null=True)
    image2 = models.ImageField('uploaded images', default= '/images/houseDefault.jpg', blank=True, null=True)
    image3 = models.ImageField('uploaded images', default= '/images/houseDefault.jpg', blank=True, null=True)
    image4 = models.ImageField('uploaded images', default= '/images/houseDefault.jpg', blank=True, null=True)
    image5 = models.ImageField('uploaded images', default= '/images/houseDefault.jpg', blank=True, null=True)

    
    def __str__(self):
        return str(self.id)
class Rating(models.Model):
    userId = models.ForeignKey(CustomUser, related_name='rating', on_delete=models.CASCADE)
    houseId = models.ForeignKey(House, related_name='rates', on_delete=models.CASCADE)
    rate = models.IntegerField(default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]) # 5 possible rating values, 1-5
    review = models.CharField(max_length=50, blank = True,  null=True)

    # def __str__(self):
    #     return self.rating

class Reservation(models.Model):
    customerId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    houseId = models.ForeignKey(House, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    checkin_date = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.status

# class HouseImages(models.Model):
#     houseId = models.ForeignKey(House, on_delete=models.CASCADE)
#     images = ListField(child=ImageField('uploaded images', default= '/images/houseDefault.jpg', blank=True, null=True))
    
    
