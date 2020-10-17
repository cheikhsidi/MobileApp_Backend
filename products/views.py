from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from PIL import Image
from django_filters import rest_framework as filters

from .serializers import ProductSerializer, RatingSerializer, ReservationSerializer, ProductSerializerDetail
from .models import Products, Rating, Reservation
# from .permissions import IsOwnerOrReadOnly
import time


class TimeDelayMixin(object, ):

    def dispatch(self, request, *args, **kwargs):
        time.sleep(3)
        return super().dispatch(request, *args, **kwargs)


class ProductFilter(filters.FilterSet):
    
    class Meta:
        model = Products
        fields = {
            'category':['iexact'],
            'title':['iexact'],
            'description':['iexact'],
            # 'carMilage':['icontains'],
            'price':['iexact', 'lte', 'gte']
        }
class MyProducts(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Products.objects.filter(customerId=user)

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)
    
    
class ModifyMyProduct(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        # CarsId = self.request.data.get('id')
        return Products.objects.filter(customerId=user)
    


class Productlist(TimeDelayMixin, ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    # filter_backends = (SearchFilter, DjangoFilterBackend)
    Search_fields = ['category', 'description', 'title', 'price']
    filter_fields = ['category', 'description', 'title', 'price']





class ProductlistDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)


class RatingView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)
