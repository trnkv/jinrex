from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^blank/$', views.get_excursion_form, name='get_excursion_form'),
	url(r'^blank/send_blank/$', views.send_excursion_form, name='send_excursion_form'),
	url(r'^blank/get_areas/$', views.get_areas),
	url(r'^schedule/$', views.view_excursions, name='view_excursions'),
	url(r'^schedule/get_excursion/(\d+)/$', views.get_excursion),
]