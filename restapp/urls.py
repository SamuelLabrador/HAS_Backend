from django.urls import path

from . import views

urlpatterns = [
	path('graph', views.graphJSON, name='graph'),
]