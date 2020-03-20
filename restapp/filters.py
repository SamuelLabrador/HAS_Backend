import django_filters

from cctv.models import *

class CCTVFilter(django_filters.FilterSet):
    class Meta:
        model = CCTV
        fields = ['county',]
