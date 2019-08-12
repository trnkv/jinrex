from django.conf.urls import url

from . import views

app_name = 'app'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^blank/$', views.get_excursion_form, name='get_excursion_form'),
	url(r'^blank/send_blank/$', views.get_excursion_form, name='get_excursion_form'),
	url(r'^blank/get_areas/$', views.get_areas),
]