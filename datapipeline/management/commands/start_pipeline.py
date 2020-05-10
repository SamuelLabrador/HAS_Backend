from django.conf import settings
from django.conf.urls.static import static
from django.core.management.base import BaseCommand

from datapipeline.pipeline import *

class Command(BaseCommand):
	help = 	'''
				This command starts the data pipeline.
			'''

	def handle(self, *args, **options):
		p = Pipeline()
		p.start()
		pass
