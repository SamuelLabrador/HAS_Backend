from django.conf import settings
from django.conf.urls.static import static
from django.core.management.base import BaseCommand

from cctv.utilities import *
from cctv.models import *

from pathlib import Path
import urllib.request
import os

class Command(BaseCommand):
	help = '''
				This command parses the CCTV objects image urls
				and saves the image to the local file system.
				The path to that image is stored with a corresponding
				Photo object in the database.

				Input: None
				Output: None
			'''

	def handle(self, *args, **options):
		
		# Get root from settings file
		root = settings.IMAGE_ROOT

		for cctv in CCTV.objects.all():

			url = cctv.image_url

			try:
				response = urllib.request.urlopen(url)	
			except Exception as e:
				continue

			image = Photo.objects.create()
			
			file_hash = generate_hash(image.id)
			
			size = len(file_hash) + len('.png')

			path = generate_path(root, file_hash) + '.png'
			directory = path[0:-size]

			Path(directory).mkdir(parents=True, exist_ok=True)
			
			print(directory)
			print(path)
			
			try:
				urllib.request.urlretrieve(url, path)
				image.file_name = file_hash
				image.cctv = cctv
				image.save()

			except Exception as e:
				print(e)
				image.delete()
