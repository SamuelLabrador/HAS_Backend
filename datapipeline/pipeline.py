from django.conf import settings
from cctv.utilities import *
from cctv.models import *
from pathlib import Path
from PIL import Image

import tensorflow as tf
import tensorflow_hub as hub
import urllib.request
import os

class Pipeline():
	def __init__(self):
		pass

	# Starts data pipeline	
	def start(self):
		saved_files = self.scrape_images()
		self.classify_images(saved_files)
	# Scrapes images
	# Indexes each image into the database
	# Derive file name for each image index
	# Saves each image with respective filename 
	def scrape_images(self):		
		# Get root from settings file
		root = settings.IMAGE_ROOT

		saved_files = []

		for cctv in CCTV.objects.all().filter(county__in=['Riverside'])[:2]:

			url = cctv.image_url

			try:
				response = urllib.request.urlopen(url)	
			except Exception as e:
				continue

			image = Photo.objects.create()
			
			file_hash = generate_hash(image.id)
			
			size = len(file_hash) + len('.png')

			path = generate_path(root, file_hash) + '.jpg'
			
			directory = path[0:-size]

			Path(directory).mkdir(parents=True, exist_ok=True)
			
			try:
				urllib.request.urlretrieve(url, path)
				image.file_name = file_hash
				image.cctv = cctv
				image.save()

				entry = {
					'path': path,
					'cctv': cctv,
					'image': image,
				}

				saved_files.append(entry)
				print("SAVING IMAGE")
			except Exception as e:
				print(e)
				image.delete()


		return saved_files

	def classify_images(self, scrape_data):
		print("CALSSIFYING IMAGES!")
		url = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
		detector = hub.load(url).signatures['default']

		def load_img(path):
			img = tf.io.read_file(path)
			img = tf.image.decode_jpeg(img, channels=3)
			return img

		for entry in scrape_data:
			image_path = entry['path']
			cctv_object = entry['cctv']
			image_object = entry['image'] 
		
			width, height = Image.open(image_path).size

			img = load_img(image_path)
			converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ]

			result = detector(converted_img)
			results = {key:value.numpy() for key, value in result.items()}


			# Extract Bounding  Box and classifications from result dictionary
			for i in range(len(results['detection_boxes'])):
				entity = results['detection_class_entities'][i]
				box = results['detection_boxes'][i]
				score = results['detection_scores'][i]

				y_min = box[0] * height
				x_min = box[1] * width
				y_max = box[2] * height
				x_max = box[3] * width

				b = [x_max, y_max, x_min, y_min]

				# Save to Database
				if entity in [b'Car', b'Land Vehicle']:
					Vehicle.objects.create(
						cctv=cctv_object,
						photo=image_object,
						x_min=x_min,
						y_min=y_min,
						x_max=x_max,
						y_max=y_max,
					)
