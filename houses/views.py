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
# from django.db.models import Avg
from PIL import Image
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters

from .serializers import HouseSerializer, RatingSerializer, ReservationSerializer, HouseSerializerDetail
from .models import House, Rating, Reservation
from .permissions import IsOwnerOrReadOnly
import time


class TimeDelayMixin(object, ):

    def dispatch(self, request, *args, **kwargs):
        time.sleep(3)
        return super().dispatch(request, *args, **kwargs)


# class ImageUploadParser(FileUploadParser):
#     media_type = 'image/*'


class HouseFilter(filters.FilterSet):
    
    class Meta:
        model = House
        fields = {
            'category':['icontains'],
            'description':['icontains'],
            'city':['icontains'],
            'area':['icontains'],
            'cost':['iexact', 'lte', 'gte']
        }
class MyHouses(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HouseSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return House.objects.filter(customerId=user)
    # parser_class = (ImageUploadParser,)
    # def put(self, request, format=None):
    #     print(request.data)
    #     if 'file' not in request.data:
    #         raise ParseError("Empty content")

    #     f = request.data['file']

    #     try:
    #         img = Image.open(f)
    #         img.verify()
    #     except:
    #         raise ParseError("Unsupported image type")

    #     House.image1.save(f.name, f, save=True)
    #     return Response(status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)
    
    
class ModifyMyHouse(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HouseSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        # houseId = self.request.data.get('id')
        return House.objects.filter(customerId=user)
    


class Houselist(TimeDelayMixin, ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filterset_class = HouseFilter
    # filter_backends = (SearchFilter, DjangoFilterBackend)
    Search_fields = ['category', 'description', 'city', 'area']
    filter_fields = ['category', 'description', 'city', 'area']





class HouselistDetail(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    queryset = House.objects.all()
    serializer_class = HouseSerializer

    # def list(self, request):
    #     queryset = House.objects.get(customerId=self.request.user)
    #     serializer = HouseSerializerDetail(queryset)
    #     return Response(serializer.data)

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = House.objects.all()
    serializer_class = HouseSerializer

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)


class RatingView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)