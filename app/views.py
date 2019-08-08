from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Excursion, Area, Facility, Organizator, Incharge, Guide

from .forms import ExcursionForm

from django.http import JsonResponse

def index(request):
    """Функция отображения для домашней страницы сайта."""
    return render(request, 'index.html', context={})


def get_excursion_form(request):
	if request.method == 'POST':
		form = ExcursionForm(request.POST)
		if form.is_valid():

			facility_id = Facility.objects.get(id_facility=request.POST.get('id_facility'))

			areas_ids = request.POST.getlist('id_area')

			print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

			guide = Guide.objects.get(id_guide=request.POST.get('id_guide'))

			print(guide)

			new_ex = Excursion.objects.create(id_facility=facility_id,
				id_guide=guide,
				name_organizator=request.POST.get('name_organizator'),
				occasion_excursion=request.POST.get('occasion_excursion'),
				date_excursion=request.POST.get('date_excursion'),
				time_period_excursion=request.POST.get('time_period_excursion'),
				language_excursion=request.POST.get('language_excursion'),
				auditory_excursion=request.POST.get('auditory_excursion'),
				participants_excursion=request.POST.get('participants_excursion'),
				age_excursion=request.POST.get('age_excursion'))

			new_ex.id_area.set(areas_ids)
			#new_ex.id_guide=guide
			new_ex.save()

			
			return render(request, 'submitted.html', context={})
	else:
		form = ExcursionForm()

	return render(request, 'excursion_form.html', {'form':form})


def submitted(request):
    """Функция отображения для домашней страницы сайта."""
    return render(request, 'submitted.html', context={})
