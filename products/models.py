from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser
# from .choices import *


class Products(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name = 'products', on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField()
    active = models.BooleanField(default=True)
    price = models.IntegerField()
    image1 = models.ImageField('uploaded images', default= '/images/productDefault.jpg', blank=True, null=True)
    image2 = models.ImageField('uploaded images', default= '/images/productDefault.jpg', blank=True, null=True)
    image3 = models.ImageField('uploaded images', default= '/images/productDefault.jpg', blank=True, null=True)
    image4 = models.ImageField('uploaded images', default= '/images/productDefault.jpg', blank=True, null=True)
    image5 = models.ImageField('uploaded images', default= '/images/productDefault.jpg', blank=True, null=True)

    
    def __str__(self):
        return str(self.id)
class Rating(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name='user_product_rating', on_delete=models.CASCADE)
    carId = models.ForeignKey(Products, related_name='product_rated', on_delete=models.CASCADE)
    rate = models.IntegerField(default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]) # 5 possible rating values, 1-5
    review = models.CharField(max_length=50, blank = True,  null=True)

    # def __str__(self):
    #     return self.rating

class Reservation(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name='user_product_reserving', on_delete=models.CASCADE)
    carId = models.ForeignKey(Products, related_name='product_reserved', on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    checkin_date = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.status

# class carImages(models.Model):
#     carId = models.ForeignKey(car, on_delete=models.CASCADE)
#     images = ListField(child=ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True))
    
    

