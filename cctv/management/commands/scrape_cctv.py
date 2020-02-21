from django.conf import settings
from django.core.management.base import BaseCommand

from cctv.models import *

import urllib.request
import json
import re

class Command(BaseCommand):
	help = 'Scapes CCTV data from the Caltrans data warehouse. Saves to database table cctv_cctv.'

	def handle(self, *args, **options):

		print('scraping cctv data.')
		for i in range(12):

			district = i + 1
			url = "http://cwwp2.dot.ca.gov/data/d{}/cctv/cctvStatusD{}.json".format(district,"%02d" % (district))
			print(url)
			try:
				with urllib.request.urlopen(url) as response:
					data = response.read().decode()
				
					json_reponse = json.loads(data)

					for device in json_reponse['data']:


						index = re.sub('[^0-9]', '', device['cctv']['index'])

						# Check if CCTV record exists already
						if CCTV.objects.filter(id=index).exists():
							continue

						loc_data = device['cctv']['location']
						img_data = device['cctv']['imageData']


						latitude = float(loc_data['latitude'])
						longitude = float(loc_data['longitude'])

						# Check if CCTV already in database.
						if CCTV.objects.all().filter(latitude__exact=latitude, longitude__exact=longitude).count() < 1:
							# Create new CCTV object
							cctv = CCTV.objects.create(
								id=index,
								latitude = latitude,
								longitude = longitude,
								district = int(loc_data['district']),
								location_name = loc_data['locationName'],
								nearby_place = loc_data['nearbyPlace'],
								elevation = int(loc_data['elevation']),
								direction = loc_data['direction'],
								county = loc_data['county'],
								route = loc_data['route'],
								route_suffix = loc_data['routeSuffix'],
								postmile_prefix = loc_data['postmilePrefix'],
								postmile = loc_data['postmile'],
								alignment = loc_data['alignment'],
								milepost = loc_data['milepost'],
								image_url = img_data['static']['currentImageURL'],
								stream_url = img_data['streamingVideoURL'],
							)
							print('+1')

			except Exception as e:
				print(device)
				print(e)
				exit(-1)	