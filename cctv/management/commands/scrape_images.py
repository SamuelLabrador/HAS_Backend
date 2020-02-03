from django.conf import settings
from django.conf.urls.static import static
from django.core.management.base import BaseCommand

from cctv.models import *
import urllib.request

class Command(BaseCommand):
	help = 'Scapes CCTV images from the Caltrans data warehouse. Saves to database table cctv_images.'

	def handle(self, *args, **options):
		count = 0
		for cctv in CCTV.objects.all():

			url = cctv.image_url
			try:
				response = urllib.request.urlopen(url)	
			except Exception as e:
				continue

			image = CCTVImage.objects.create()
			
			file_name = str(image.id) + '.png'
			path = settings.STATIC_ROOT+'images/cctv/' + file_name
			try:
				urllib.request.urlretrieve(url, path)
				image.path = path
				image.save()
				
			except Exception as e:
				print(e)
				image.delete()
