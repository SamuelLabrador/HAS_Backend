from rest_framework import serializers
from cctv.models import CCTV

class CCTVSerializers(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ('id','longitude','latitude','route','image_url')
        