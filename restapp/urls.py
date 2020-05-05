from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('cctv', views.CCTVViewSet)
router.register('search', views.SearchViewSet, 'search')
router.register('vehicle', views.VehicleViewSet, 'vehicle')

urlpatterns = [
	path('graph', cache_page(60 * 60 * 24)(views.graphJSON), name='graph'),
	path('routeVehicleCount', cache_page(60 * 15)(views.routeVehicleCount), name='routeVehicleCount'),
	path('totalVehicle', cache_page(60 * 2)(views.totalVehicle), name='totalVehicle'),
	path('vehiclesPerHour', cache_page(60 * 60)(views.vehiclesPerHour), name='vehiclesPerHour'),
	path('vehiclesPerCCTV', cache_page(60 * 15)(views.vehiclesPerCCTV), name='vehiclesPerCCTV'),
	path('trafficData', views.trafficData, name='trafficData'),
]

urlpatterns += router.urls