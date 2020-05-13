import memcache
import json
from cctv.models import *
from django.conf import settings
from django.utils import timezone

def getRouteVehicleCount(update=False):
    mc = memcache.Client(['cache:11211'], debug=0)
    key = 'routeVehicleCount'
    result = mc.get(key)

    if result is None or update:
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
        result = json.dumps(routes)
        mc.set(key, result, 60*15)

    data = json.loads(result)
    return data

def getTrafficData(update=False):
    mc = memcache.Client(['cache:11211'], debug=0)
    key = 'trafficDataResponse'
    result = mc.get(key)
    result
    if result is None or update:
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

        result = json.dumps(data)
        mc.set(key, result, time=60*15)
    
    data = json.loads(result)
    return data
    
def getGraph(update=False):
    mc = memcache.Client(['cache:11211'], debug=0)
    key = 'graphJSON'
    result = mc.get(key)

    if result == None or update:
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

        result = json.dumps(routes)
        mc.set(key, result, 60 * 15)

    data = json.loads(result)
    return data

def getVehiclesPerHour(update=False):
    mc = memcache.Client(['cache:11211'], debug=0)
    key = 'vehiclesPerHour'
    result = mc.get(key)

    if result is None or update:
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
        result = json.dumps(data)
        mc.set(key, result, 60*15)

    return json.loads(result)
    
def getVehiclesPerCCTV(update=False):
    mc = memcache.Client(['cache:11211'], debug=0)
    key = 'vehiclesPerCCTV'
    result = mc.get(key)

    if result is None or update:
        objects = CCTV.objects.all().filter(county__in=settings.VALID_COUNTIES)
        target_timezone = timezone.now() - timezone.timedelta(days=1)

        routes = {}

        for meta in objects:
            count = Vehicle.objects.all().filter(cctv__exact=meta)
            count = count.filter(timestamp__gt=target_timezone)
            count = count.count()
            routes[meta.id] = count
        
        result = json.dumps(routes)
        mc.set(key, result, 60*15)
    
    return json.loads(result)
    