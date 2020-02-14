from django.urls import path, re_path

from . import views

urlpatterns = [
	re_path(r'[0-9a-f]*', views.image, name='image')
]
