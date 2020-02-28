import django_filters
from django_filters import rest_framework as filters
from django_filters.fields import Lookup

from cctv.models import CCTV

# class MultiValueCharFilter(filters.CharFilter):
#     def filter(self, qs, value):
#         # value is either a list or an 'empty' value
#         values = value or []

#         for value in values:
#             print(value)
#             qs = super(MultiValueCharFilter, self).filter(qs, value)
        
#         return qs

class CCTVFilter(django_filters.FilterSet):

    class Meta:
        model = CCTV
        fields = ['county',]

    
# class ListFilter(Filter):
#     def filter(self, qs, value):
#         value_list = value.split(u',')
#         return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))

# class ProductFilterSet(django_filters.FilterSet):
#     county = ListFilter(field_name='county')

#     class Meta:
#         model = CCTV
#         fields = ['county',]