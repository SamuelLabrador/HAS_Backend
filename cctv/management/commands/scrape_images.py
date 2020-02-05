from django.conf import settings
from django.conf.urls.static import static
from django.core.management.base import BaseCommand

from cctv.models import *
from pathlib import Path
import urllib.request

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
		count = 0
		parent_directory = settings.STATIC_ROOT+'images/cctv/'
		Path(parent_directory).mkdir(parents=True)

		for cctv in CCTV.objects.all():

			url = cctv.image_url
			try:
				response = urllib.request.urlopen(url)	
			except Exception as e:
				continue

			image = Photo.objects.create()
			
			file_name = str(image.id) + '.png'
			path = parent_directory + file_name

			try:
				urllib.request.urlretrieve(url, path)
				image.path = path
				image.save()
				
			except Exception as e:
				print(e)
				image.delete()
