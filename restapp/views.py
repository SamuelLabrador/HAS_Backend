from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CCTVSerializers, SearchSerializers, VehicleSerializers
from cctv.models import CCTV,Photo,Vehicle
from .filters import CCTVFilter

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