from django.contrib import admin
from cctv.models import CCTV, Photo, Vehicle

# Register your models here.
@admin.register(CCTV)
class CCTVInline(admin.ModelAdmin):
	model = CCTV
	list_display = ('location_name', 'latitude', 'longitude', 'route', 'county',)

@admin.register(Photo)
class PhotoInline(admin.ModelAdmin):
	model = Photo
	list_display = ('id', 'cctv', 'file_name', 'timestamp', 'vehicle_count')

@admin.register(Vehicle)
class VehicleInLine(admin.ModelAdmin):
	model = Vehicle
	list_display = ('id', 'label', 'probability', 'cctv', 'photo', 'x_min', 'y_min','x_max', 'y_max', 'timestamp')