from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CCTVSerializers, PhotoSerializers
from cctv.models import CCTV,Photo

# Create your views here.

class CCTVViewSet(viewsets.ModelViewSet):

    queryset = CCTV.objects.all()
    serializer_class = CCTVSerializers

class PhotoViewSet(viewsets.ModelViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializers