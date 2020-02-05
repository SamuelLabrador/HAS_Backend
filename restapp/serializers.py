from rest_framework import serializers
from cctv.models import CCTV, Photo

class CCTVSerializers(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ('id','longitude','latitude','route','image_url')

class PhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id','cctv','path','timestamp')