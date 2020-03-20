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

import string
import json
import re

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    # Create your views here.
class MediumResultsSetPagination(PageNumberPagination):
    page_size = 25
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
    serializer_class = VehicleSerializers 
    filter_backends = (filters.SearchFilter, )
    search_fields = ['photo__file_name']
    pagination_class = MediumResultsSetPagination


def graphJSON(request):

    queryset = CCTV.objects.all().filter(county__in=settings.VALID_COUNTIES)
    route_values = queryset.values('route').distinct()
    
    special_case = {
        'SR-91': 'longitude'
    }

    routes = dict()

    for route_set in route_values:
        string_route = route_set['route']
        route = string_route

        if route in special_case:
            direction = special_case[route]

        else:
            num = ''
            for c in route:
                if c.isdigit():
                    num += c

            num = int(num)
            
            if num % 2 == 0:
                direction = 'longitude'
            else:
                direction = 'latitude'

        cctvs = queryset.filter(route__exact=route).order_by(direction)

        objects = []
        for cctv in cctvs:
            json_object = {
            	'cctv_id': (cctv.id),
            	'latitude': (cctv.latitude), 
            	'longitude': (cctv.longitude),
            }
            objects.append(json_object)
        routes[string_route] = objects

    return JsonResponse(routes, safe=False)

def routeVehicleCount(request):
    
    objects = CCTV.objects.all().filter(county__in=settings.VALID_COUNTIES)
    objects = objects.values('route').distinct()
    target_timezone = timezone.now() - timezone.timedelta(days=1)
    
    routes = {}
    for meta in objects:
        route = meta['route']

        cctvs = CCTV.objects.all().filter(route__exact=route)
 
        count = Vehicle.objects.all().filter(cctv__in=cctvs)
        count = count.filter(timestamp__gt=target_timezone)
        count = count.count()

        routes[route] = count

    return JsonResponse(routes, safe=False)

def totalVehicle(request):
    count = Vehicle.objects.all().count()

    total = {
        'count' : count
    }

    return JsonResponse(total, safe=False)

def vehiclesPerHour(request):
	now = timezone.now()
	
	route_values = CCTV.objects.all().filter(county__in=settings.VALID_COUNTIES)
	route_values = [i for i in route_values.values('route').distinct()]

	data = {}

	for tup in route_values:
		route = tup['route']
		counts = []
		for i in range(24, 0, -1):
			start = now - timezone.timedelta(hours=i)
			end = start + timezone.timedelta(hours=1)

			cctvs = CCTV.objects.all().filter(route__exact=route)
			photos = Photo.objects.all().filter(timestamp__gte=start).filter(timestamp__lt=end).filter(cctv__in=cctvs)

			counts.append(Vehicle.objects.all().filter(photo__in=photos).count())

		data[route] = counts

	return JsonResponse(data, safe=False)

def vehiclesPerCCTV(request):
    valid_counties = [
        'San Bernardino',
        'Riverside'
    ]

    
    objects = CCTV.objects.all().filter(county__in=valid_counties)
    target_timezone = timezone.now() - timezone.timedelta(days=1)

    routes = {}

    for meta in objects:
        count = Vehicle.objects.all().filter(cctv__exact=meta)
        count = count.filter(timestamp__gt=target_timezone)
        count = count.count()
        routes[meta.id] = count


    return JsonResponse(routes, safe=False)

'''
	[
		cctv_id : xxx,
		car_count: xxx
	],
'''

def trafficData(request):
	data = []
	for cctv in CCTV.objects.all().filter(county__in=settings.VALID_COUNTIES):

		candiates = Photo.objects.all().filter(cctv__exact=cctv).order_by('-id')

		if candiates.count() > 0:
			photo = Photo.objects.all().filter(cctv__exact=cctv).order_by('-timestamp')[0]
			if photo.vehicle_count == None:
				photo = Photo.objects.all().filter(cctv__exact=cctv).order_by('-timestamp')[1]
			data.append({
				'cctv_id' : cctv.id,
				'car_count' : photo.vehicle_count,
			})
	
	return JsonResponse(data, safe=False)


