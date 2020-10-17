from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import Productlist, ProductlistDetail, MyProducts, ModifyMyProduct, RatingView


urlpatterns = [

    # path("houses/", HouseList.as_view(), name="Houses_list"),
    path("products/", Productlist.as_view(), name="products"),
    path("products/<int:pk>/", ProductlistDetail.as_view(), name = "product_details"),
    path("myproducts/", MyProducts.as_view(), name="my_products"),
    # path("myhouses/modify/", ModifyMyHouse.as_view(), name="create_house"),
    path("myproducts/<int:pk>/", ModifyMyProduct.as_view(), name="update_product"),
    path("product/<int:pk>/rates/", RatingView.as_view({'get': 'list'}), name="rating"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
