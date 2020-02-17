from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
	url(r'^$', views.index, name='jinrex'),
	url(r'^profile/(\d+)/$', views.profile, name='profile'),
	url(r'^blank/$', views.get_excursion_form, name='get_excursion_form'),
	url(r'^blank/send_blank/$', views.send_excursion_form, name='send_excursion_form'),
	url(r'^blank/get_areas/$', views.get_areas),
	url(r'^schedule/$', views.view_excursions, name='view_excursions'),
	url(r'^schedule/get_excursion/(\d+)/$', views.get_excursion),
	url(r'^schedule/get_excursion/(\d+)/change_confirmed/$', views.change_confirmed),
	url(r'^schedule/get_excursion/(\d+)/mark_as_not_held/$', views.mark_as_not_held),
	url(r'^schedule/get_excursion/(\d+)/send_message/(\d+)/$', views.send_message),
	url(r'^change_excursion/(\d+)/$', views.change_excursion, name='change_excursion'),
	url(r'^schedule/get_excursion/(\d+)/create_chat/(\d+)/$', views.create_chat),
	url(r'^facilities/', views.view_facilities_attendace, name='view_facilities_attendace'),
	url(r'^areas/', views.view_areas_attendace, name='view_areas_attendace'),
	url(r'^guides/', views.view_guide_statistics, name='view_guide_statistics'),
	url(r'^calendar/', views.view_calendar, name='view_calendar')
]
