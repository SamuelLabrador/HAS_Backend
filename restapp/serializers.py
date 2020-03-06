from rest_framework import serializers
from cctv.models import CCTV, Photo, Vehicle

class CCTVSerializers(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ('id','longitude','latitude','route','image_url', 'county')

class SearchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id','cctv','file_name','timestamp')

class VehicleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id','cctv','photo','x_min','y_min','x_max','y_max', 'timestamp')