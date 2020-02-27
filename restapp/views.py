from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CCTVSerializers, SearchSerializers
from cctv.models import CCTV,Photo
from .filters import CCTVFilter

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CCTVViewSet(viewsets.ModelViewSet):

    queryset = CCTV.objects.all()
    serializer_class = CCTVSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = CCTVFilter

class SearchViewSet(viewsets.ModelViewSet):
    
    queryset = Photo.objects.all().order_by('-timestamp')
    serializer_class = SearchSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['=cctv__id',]
    pagination_class = StandardResultsSetPagination