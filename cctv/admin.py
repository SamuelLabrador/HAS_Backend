from django.contrib import admin
from cctv.models import CCTV, Photo


# Register your models here.
@admin.register(CCTV)
class CCTVInline(admin.ModelAdmin):
	model = CCTV
	list_display = ('location_name', 'latitude', 'longitude', 'route', 'county',)

@admin.register(Photo)
class PhotoInline(admin.ModelAdmin):
	model = Photo
	list_display = ('id', 'cctv', 'file_name', 'timestamp')

