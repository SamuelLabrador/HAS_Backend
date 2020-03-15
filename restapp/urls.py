from django.urls import path

from . import views

urlpatterns = [
	path('graph', views.graphJSON, name='graph'),
	path('routeVehicleCount', views.routeVehicleCount, name='routeVehicleCount'),
	path('totalVehicle', views.totalVehicle, name='totalVehicle'),
	path('vehiclesPerHour', views.vehiclesPerHour, name='vehiclesPerHour'),
]