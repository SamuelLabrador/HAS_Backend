from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings

from .utilities import decode_path, generate_hash

# Create your views here.
def cctv(request):
	return render(request, 'cctv/cctv.html')

def image(request):
	uri = request.build_absolute_uri()
	hash_start = uri.rfind('/')
	print(hash_start)

	print(uri[hash_start + 1:])
	# file_hash = generate_hash(uri[hash_start + 1:])
	file_hash = uri[hash_start + 1:]
	# path = decode_path(settings.IMAGE_URL, file_hash) + '.jpg'
	path = settings.IMAGE_URL + '/' + file_hash[0:2] + '/' + file_hash[2:4] + '/' + file_hash + '.jpg'
	print(path)
	return HttpResponseRedirect(path)

