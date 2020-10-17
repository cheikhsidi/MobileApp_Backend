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

from .serializers import CarSerializer, RatingSerializer, ReservationSerializer, CarSerializerDetail
from .models import Cars, Rating, Reservation
# from .permissions import IsOwnerOrReadOnly
import time


class TimeDelayMixin(object, ):

    def dispatch(self, request, *args, **kwargs):
        time.sleep(3)
        return super().dispatch(request, *args, **kwargs)


# class ImageUploadParser(FileUploadParser):
#     media_type = 'image/*'


class CarFilter(filters.FilterSet):
    
    class Meta:
        model = Cars
        fields = {
            'carMake':['iexact'],
            'carModel':['iexact'],
            'carYear':['iexact'],
            # 'carMilage':['icontains'],
            'price':['iexact', 'lte', 'gte']
        }
class MyCars(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Cars.objects.filter(customerId=user)
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

    #     Cars.image1.save(f.name, f, save=True)
    #     return Response(status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)
    
    
class ModifyMyCar(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer
    # lookup_field = 'id'
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        # CarsId = self.request.data.get('id')
        return Cars.objects.filter(customerId=user)
    


class Carlist(TimeDelayMixin, ListAPIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
    filterset_class = CarFilter
    # filter_backends = (SearchFilter, DjangoFilterBackend)
    Search_fields = ['category', 'description', 'city', 'area']
    filter_fields = ['category', 'description', 'city', 'area']





class CarlistDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cars.objects.all()
    serializer_class = CarSerializer

    # def list(self, request):
    #     queryset = Cars.objects.get(customerId=self.request.user)
    #     serializer = CarSerializerDetail(queryset)
    #     return Response(serializer.data)

class CarViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Cars.objects.all()
    serializer_class = CarSerializer

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)


class RatingView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(customerId=self.request.user)
