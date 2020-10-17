from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import CustomUser
# from .choices import *


class Cars(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name = 'cars', on_delete=models.CASCADE)
    # location = models.CharField(max_length=100, blank=True, null=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    # subArea = models.CharField(max_length=50)
    fuelType = models.CharField(max_length=50)
    carMake = models.CharField(max_length=50)
    carModel = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    carYear = models.IntegerField()
    carMilage = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    image1 = models.ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True)
    image2 = models.ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True)
    image3 = models.ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True)
    image4 = models.ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True)
    image5 = models.ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True)

    
    def __str__(self):
        return str(self.id)
class Rating(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name='user_car_rating', on_delete=models.CASCADE)
    carId = models.ForeignKey(Cars, related_name='car_rated', on_delete=models.CASCADE)
    rate = models.IntegerField(default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)]) # 5 possible rating values, 1-5
    review = models.CharField(max_length=50, blank = True,  null=True)

    # def __str__(self):
    #     return self.rating

class Reservation(models.Model):
    customerId = models.ForeignKey(CustomUser, related_name='user_car_reserving', on_delete=models.CASCADE)
    carId = models.ForeignKey(Cars, related_name='car_reserved', on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    checkin_date = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.status

# class carImages(models.Model):
#     carId = models.ForeignKey(car, on_delete=models.CASCADE)
#     images = ListField(child=ImageField('uploaded images', default= '/images/carDefault.jpg', blank=True, null=True))
    
    

