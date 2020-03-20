from django.urls import path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('cctv', views.CCTVViewSet)
router.register('search', views.SearchViewSet, 'search')
router.register('vehicle', views.VehicleViewSet, 'vehicle')

urlpatterns = [
	path('graph', views.graphJSON, name='graph'),
	path('routeVehicleCount', views.routeVehicleCount, name='routeVehicleCount'),
	path('totalVehicle', views.totalVehicle, name='totalVehicle'),
	path('vehiclesPerHour', views.vehiclesPerHour, name='vehiclesPerHour'),
	path('vehiclesPerCCTV', views.vehiclesPerCCTV, name='vehiclesPerCCTV'),
	path('trafficData', views.trafficData, name='trafficData'),
]

urlpatterns += router.urls