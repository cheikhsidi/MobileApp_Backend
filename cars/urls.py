from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import Carlist, CarlistDetail, MyCars, ModifyMyCar, RatingView


urlpatterns = [

    # path("houses/", HouseList.as_view(), name="Houses_list"),
    path("cars/", Carlist.as_view(), name="cars"),
    path("cars/<int:pk>/", CarlistDetail.as_view(), name = "car_details"),
    path("mycars/", MyCars.as_view(), name="my_cars"),
    # path("myhouses/modify/", ModifyMyHouse.as_view(), name="create_house"),
    path("mycars/<int:pk>/", ModifyMyCar.as_view(), name="update_car"),
    path("rates/", RatingView.as_view({'get': 'list'}), name="rating"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
