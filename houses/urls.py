from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [

    # path("houses/", HouseList.as_view(), name="Houses_list"),
    path("houses/", Houselist.as_view(), name="houses"),
    path("houses/<int:pk>/", HouselistDetail.as_view(), name = "house_details"),
    path("myhouses/", MyHouses.as_view(), name="my_houses"),
    # path("myhouses/modify/", ModifyMyHouse.as_view(), name="create_house"),
    path("myhouses/<int:pk>/", ModifyMyHouse.as_view(), name="update_house"),
    path("rates/", RatingView.as_view({'get': 'list'}), name="rating"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
