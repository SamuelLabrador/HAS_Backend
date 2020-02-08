from django.test import TestCase
from rest_framework.test import APIRequestFactory

import json
from cctv.models import *

# Create your tests here.

class RestAppTestCase(TestCase):
	def setUp(self):
		CCTV.objects.create(
			district=1,
			longitude=1,
			latitude=1,
			elevation=1,
		)

	def test_request(self):
		factory = APIRequestFactory()
		response = self.client.get('/api/cctv/')

		cctv = json.loads(json.dumps(response.data))[0]
		
		self.assertTrue(cctv['latitude'] == 1)
		self.assertTrue(cctv['longitude'] == 1)
		