from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.test import Client

import json
from cctv.models import CCTV, Photo, Vehicle

# Create your tests here.

class RestAppTestCase(TestCase):
	fixtures = [
		'test/cctv_test.json',
		'test/photo_test.json',
		'test/vehicle_test.json'
	]

	def setUp(self):
		# Initialize Client
		self.clients = Client()

		# Load objects into models.
		self.c = CCTV.objects.all()
		self.p = Photo.objects.all()
		self.v = Vehicle.objects.all()

		# Validate fixtures have been loaded properly
		self.assertEqual(self.c.get(id=1), self.p.get(id=1).cctv, msg="Photo.cctv must be equal to corresponding cctv object")
		self.assertEqual(self.v.get(id=1).cctv, self.c.get(id=1))
		self.assertEqual(self.v.get(id=1).photo, self.p.get(id=1))

	'''
	Test checks total vehicle api endpoint
	'''
	def testTotalVehicle(self):
		response = self.client.get('/api/totalVehicle')
		self.assertEqual(response.json()['count'], 3)

	'''
	Test checks validity of data returned from vehicle api endpoint
	'''
	def testVehicleViewSet(self):
		def helper(cctv_id):
			response = self.client.get('/api/vehicle/?format=json&cctv={}'.format(cctv_id))
			vehicles = response.json()['results']
			for v in vehicles:
				self.assertEqual(v['cctv'], cctv_id)
		
		# Test both functions
		helper(1)
		helper(2)

		# Response should not be cached
		helper(1)