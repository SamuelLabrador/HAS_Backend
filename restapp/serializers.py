from rest_framework import serializers
from cctv.models import CCTV, Photo

class CCTVSerializers(serializers.ModelSerializer):
    class Meta:
        model = CCTV
        fields = ('id','longitude','latitude','route','image_url')

class PhotoSerializers(serializers.ModelSerializer):
    # we could just refer to cctv id, dont have to overwrite
    cctv = serializers.CharField(source='cctv.image_url')

    class Meta:
        model = Photo
        fields = ('id','cctv','file_name','timestamp')

class SearchSerializers(serializers.ModelSerializer):
    #cctv = serializers.CharField(source='cctv.image_url')

    class Meta:
        model = Photo
        fields = ('id','cctv','file_name','timestamp')