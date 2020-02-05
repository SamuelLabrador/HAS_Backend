from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CCTVSerializers
from cctv.models import CCTV

# Create your views here.

class CCTVViewSet(viewsets.ModelViewSet):

    queryset = CCTV.objects.all()
    serializer_class = CCTVSerializers