from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .utilities import decode_path

# Create your views here.
def cctv(request):
	return render(request, 'cctv/cctv.html')

def image(request):
	uri = request.build_absolute_uri()
	hash_start = uri.rfind('/')
	file_hash = uri[hash_start + 1:]

	path = decode_path(settings.IMAGE_ROOT, file_hash) + '.png'

	response = HttpResponse()
	response['X-Accel-Redirect'] = path 
	return HttpResponse(path)
