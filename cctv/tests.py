from django.test import TestCase

from .models import *
from .utilities import *

class CCTVUtilityTestCase(TestCase):
	def setUp(self):
		
		# Create 6 Fake CCTV Cameras
		self.coordinate_list = [
			(34.081538, -117.70403),
			(34.082252, -117.69605),
			(34.085001, -117.69013),
			(34.083304, -117.63272),
			(34.067296, -117.5847),
			(34.065084, -117.31259),
		]

		for i, coordinate in enumerate(self.coordinate_list):
			cctv = CCTV.objects.create(
				district=i, 
				location_name ='Location {}'.format(i),
				nearby_place ='Nearby Place {}'.format(i),
				latitude = coordinate[0],
				longitude = coordinate[1],
				elevation = 1000,
				direction = 'West {}'.format(i),
				county = 'SBD/RIV {}'.format(i),
				route = 'ROUTE-{}'.format(i),
				route_suffix = 'SUFFIX-{}'.format(i),
				postmile_prefix = 'PREFIX-{}'.format(i),
				postmile = 'POSTMILE-{}'.format(i),
				alignment = 'ALIGNMENT-{}'.format(i),
				milepost = 'MILEPOST-{}'.format(i),
				image_url = 'URL-{}'.format(i),
				stream_url= 'URL-{}'.format(i),
			)
		
	def tearDown(self):
		for camera in CCTV.objects.all():
			camera.delete()

	def test_cctv_instantiation(self):
		all_tvs = CCTV.objects.all()
		
		self.assertEqual(all_tvs.count(), len(self.coordinate_list), "6 six CCTVs need to be instantiated")

		# Query the coordinate list to find the CCTVs that have been instantiated
		for lat, lng in self.coordinate_list:

			# Filter the CCTVs based on lat, lng
			tv = all_tvs.filter(latitude__exact=lat, longitude__exact=lng)
			self.assertEqual(tv.count(), 1, "A CCTV has not been found, {} {}".format(lat, lng))

	def test_get_nearby_cameras(self):
		
		# Offset the lat, lng
		offset = 0.00001
	
		for lat, lng in self.coordinate_list:
			closest_cctv = CCTV.objects.get(latitude=lat, longitude=lng)
				
			# Returns [(distance, CCTV),]
			cameras = get_nearby_cameras(lat + offset, lng + offset)
		
			self.assertEqual(closest_cctv, cameras[0][1])
