from django.shortcuts import render
from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CCTVSerializers, PhotoSerializers, SearchSerializers
from cctv.models import CCTV,Photo

# Create your views here.
class CCTVViewSet(viewsets.ModelViewSet):

    queryset = CCTV.objects.all()
    serializer_class = CCTVSerializers

class PhotoViewSet(viewsets.ModelViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializers

class SearchViewSet(viewsets.ModelViewSet):

    #queryset = Photo.objects.all()
    
    serializer_class = SearchSerializers

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    search_fields = ['=cctv__id',]

    def get_queryset(self):
        #num = self.request.query_params.get('num')
        
        

        #if not num:
        #    qset = Photo.objects.all()
        #else:
        #    qset = Photo.objects.all()[:int(num)]

        #queryset = qset

        #q = Photo.objects.all()
        #queryset = q[:int(num)]

        #queryset = Photo.objects.filter(pk__in = Photo.objects.all()[:int(num)+1].values_list('pk'))
        #queryset = Photo.objects.all()[:int(num):1]

        
        num = self.request.query_params.get('num')
        search = self.request.query_params.get('search')
        print(search)

        query = Photo.objects.all()
        
        if not num:
            queryset = query
        else:
            #queryset = Photo.objects.filter(Photo.objects.all()[:int(num)+1])
            queryset = query.filter(cctv__exact=int(search))[:int(2)]

        return queryset
    