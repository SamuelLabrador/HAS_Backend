from django.db import models

# Create your models here.

# Physical Device Information
class CCTV(models.Model):
	district = models.IntegerField()
	location_name = models.CharField(max_length=255, blank=True, null=True)
	nearby_place = models.CharField(max_length=255, blank=True, null=True)
	
	longitude = models.FloatField()
	latitude = models.FloatField()
	
	elevation = models.IntegerField()
	direction = models.CharField(max_length=255, blank=True, null=True)
	county = models.CharField(max_length=255, blank=True, null=True)

	route = models.CharField(max_length=255, blank=True, null=True)
	route_suffix = models.CharField(max_length=255, blank=True, null=True)

	postmile_prefix = models.CharField(max_length=255, blank=True, null=True)
	postmile = models.CharField(max_length=255, blank=True, null=True)

	alignment = models.CharField(max_length=255, blank=True, null=True)
	milepost = models.CharField(max_length=255, blank=True, null=True)

	image_url = models.CharField(max_length=255, blank=True, null=True)
	stream_url = models.CharField(max_length=255, blank=True, null=True)

# History of image
class CCTVImage(models.Model):
	cctv = models.ForeignKey(CCTV, null=True, on_delete=models.SET_NULL)
	path = models.CharField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
