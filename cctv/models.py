from django.db import models

# Create your models here.

# Physical Device Information
class CCTV(models.Model):
	district = models.IntegerField()
	location_name = models.CharField(max_length=255, blank=True, null=True)
	nearby_place = models.CharField(max_length=255, blank=True, null=True)
	
	longitude = models.FloatField()
	latitude = models.FloatField()
	
	elevation = models.FloatField()
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

	def __str__(self):
		return self.location_name

# History of image
class Photo(models.Model):
	cctv = models.ForeignKey(CCTV, null=True, on_delete=models.SET_NULL)
	file_name = models.CharField(max_length=255, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	vehicle_count = models.IntegerField(null=True, blank=True)

# Vehicle Classifications
class Vehicle(models.Model):
	cctv = models.ForeignKey(CCTV, null=True, on_delete=models.SET_NULL)
	photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL)
	
	# Bounding Boxes
	x_min = models.FloatField()
	y_min = models.FloatField()
	x_max = models.FloatField()
	y_max = models.FloatField()

	timestamp = models.DateTimeField(auto_now_add=True)
	