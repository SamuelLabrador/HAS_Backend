from django.urls import path

from . import views

urlpatterns = [
	path('', views.cctv, name='cctv'),
]
