from django.conf.urls import url

from . import views

app_name = 'app'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^blank/$', views.get_excursion_form, name='get_excursion_form'),
	url(r'^blank/send_blank/$', views.send_excursion_form, name='send_excursion_form'),
	url(r'^blank/get_areas/$', views.get_areas),
	url(r'^schedule/$', views.view_excursions, name='view_excursions'),
	url(r'^schedule/update_excursion/', views.update_excursion, name='update_excursion'),
]