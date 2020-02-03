from django.shortcuts import render

# Create your views here.
def cctv(request):
	return render(request, 'cctv/cctv.html')