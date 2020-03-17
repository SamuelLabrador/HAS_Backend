from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CCTVSerializers, SearchSerializers, VehicleSerializers
from cctv.models import CCTV,Photo,Vehicle
from .filters import CCTVFilter
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

import string
import json
import re

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
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
    queryset = Photo.objects.all().order_by('-timestamp')
    serializer_class = SearchSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['=cctv__id',]
    pagination_class = StandardResultsSetPagination

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('-timestamp')
    serializer_class = VehicleSerializers    
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['photo', 'cctv']
    pagination_class = StandardResultsSetPagination

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
    #routes_list = []
    for meta in objects:
        count = Vehicle.objects.all().filter(cctv__exact=meta)
        count = count.filter(timestamp__gt=target_timezone)
        count = count.count()
        routes[meta.id] = count
        #routes_list.append({meta.id : count})

    return JsonResponse(routes, safe=False)