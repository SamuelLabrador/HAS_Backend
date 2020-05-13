from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from rest_framework import viewsets, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from cctv.models import CCTV,Photo,Vehicle
from .filters import CCTVFilter
from .api_caching import *

import string
import json
import re

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class MediumResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CCTVViewSet(viewsets.ModelViewSet):
    serializer_class = CCTVSerializers
    queryset = CCTV.objects.all()
    def get_queryset(self):
        queryset = CCTV.objects.all()

        county_param = self.request.query_params.get('county', None)

        # Check if no county param is passed in
        if county_param is None:
            return queryset

        elif ',' in county_param:
            county_param = county_param.split(',')
            return queryset.filter(county__in=county_param)
        
        return queryset.filter(county__exact=county_param)

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().filter(vehicle_count__isnull=False).order_by('-timestamp')
    serializer_class = PhotoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['=cctv__id',]
    pagination_class = StandardResultsSetPagination

class VehicleViewSet(viewsets.ModelViewSet):
    """
    Pass in the image file_name.
    Return Corresponding bounding boxes.
    """
    queryset = Vehicle.objects.all().order_by('-timestamp')
    def get_queryset(self):
        return Vehicle.objects.all().order_by('-timestamp')

    serializer_class = VehicleSerializers 
    filter_backends = (filters.SearchFilter, )
    search_fields = ['photo__file_name']
    pagination_class = MediumResultsSetPagination

'''
BEGIN CUSTOM APIs
'''

def graphJSON(request):
   
    data = getGraph()

    return JsonResponse(data, safe=False)

'''
This API counts the amount of cars on each route
Should be cached to minimze load on server. Updates every ~15 minutes. 

TODO: Add ability to pass in specified interval.
'''
def routeVehicleCount(request):
    data = getRouteVehicleCount()
    return JsonResponse(data, safe=False)

'''
Returns total amount of vehicle objects in the database
'''
def totalVehicle(request):
    count = Vehicle.objects.all().count()
    total = {
        'count' : count
    }
    return JsonResponse(total, safe=False)

'''
This request gets the total amount of vehicles from the previous hour. 

TODO: Use rounded hours. ie current time == 2:30, then range(1:00 - 2:00)
'''
def vehiclesPerHour(request):
	data = getVehiclesPerHour()
	return JsonResponse(data, safe=False)

def vehiclesPerCCTV(request):
    valid_counties = [
        'San Bernardino',
        'Riverside'
    ]

    data = getVehiclesPerCCTV()


    return JsonResponse(data, safe=False)

'''
	[
		cctv_id : xxx,
		car_count: xxx
	],
'''

def trafficData(request):
    data = getTrafficData()
    return JsonResponse(data, safe=False)