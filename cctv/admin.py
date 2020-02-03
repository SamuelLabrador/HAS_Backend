from django.contrib import admin
from cctv.models import CCTV, Image

# Register your models here.
@admin.register(CCTV)
class CCTVInline(admin.ModelAdmin):
	model = CCTV
	list_display = ('location_name', 'latitude', 'longitude', 'route', 'county',)

admin.site.register(Image)

