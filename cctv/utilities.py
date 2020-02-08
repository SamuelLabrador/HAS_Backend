from .models import *
from math import radians, sin, cos, asin, sqrt
import hashlib

# MILES
EARTH_RADIUS = 3956

def haversine(lat1, lng1, lat2, lng2):
	dlng = lng2 - lng1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
	c = 2 * asin(sqrt(a)) * EARTH_RADIUS
	return c
	
def get_nearby_cameras(lat, lng):
	cameraList = list()

	# GET QUERYSET OF CCTVS
	cctvs = CCTV.objects.all()

	for cctv in cctvs:
		cctvLat = cctv.latitude
		cctvLng = cctv.longitude

		distance = haversine(lat, lng, cctvLat, cctvLng)
		cameraList.append((distance, cctv))

	def getKey(arr):
		return arr[0]

	cameraList.sort(key=getKey)
	return cameraList

# Utility functions for storing images
# generate_hash()
# generate_path()
# decode_path()
def generate_hash(index):
	m = hashlib.sha1()
	m.update(str(index).encode())
	return m.hexdigest()

def generate_path(root, file_hash):
	h = file_hash
	path = root + '/' + h[0:2] + '/' + h[2:4] + '/'	+ file_hash
	return path
	
def decode_path(root, file_hash):
	dirs = file_hash[0:2] + '/' + file_hash[2:4] + '/'
	return root + dirs + file_hash
