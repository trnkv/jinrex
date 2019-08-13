from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import JsonResponse

from .models import Excursion, Area, Facility, Organizator, Incharge, Guide
from .forms import ExcursionForm
from .delete import ExcursionDelete

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Функция отображения для домашней страницы сайта."""
    return render(request, 'index.html', context={})


@login_required
def get_areas(request):
	if request.method == 'POST':
		if 'id_facility' in request.POST:
			id_facility = request.POST.get('id_facility')
			list_of_dict_areas = list(Area.objects.filter(id_facility=id_facility).values('name_area'))
			areas = []
			for d in list_of_dict_areas:
				areas.append(d['name_area'])
			return JsonResponse({'result':areas})
			#return render_to_response('excursion_form.html', {'areas': areas})


@login_required
def get_excursion_form(request):
	if request.method == 'POST':
		form = ExcursionForm(request.POST)
		if form.is_valid():

			facility_id = Facility.objects.get(id_facility=request.POST.get('id_facility'))

			areas_ids = request.POST.getlist('id_area')

			guide = Guide.objects.get(id_guide=request.POST.get('id_guide'))

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

@login_required
def submitted(request):
    """Функция отображения успешной отправки заявки на экскурсию."""
    return render(request, 'submitted.html', context={})

@login_required
def view_excursions(request):
	excursions = Excursion.objects.all().values()
	excursions = [val for val in excursions if val in excursions]

	excursions_all = dict()

	for d in excursions:

		this_facilities = list(Facility.objects.filter(id_facility=d['id_facility_id']).values('name_facility'))
		this_areas = list(Area.objects.filter(id_facility=d['id_facility_id']).values('name_area'))
		this_organizator = d['name_organizator']
		this_guide = list(Guide.objects.filter(id_guide=d['id_guide_id']).values('lastName_guide'))
		this_occasion = d['occasion_excursion']
		this_date = d['date_excursion']
		this_time = d['time_period_excursion']
		this_language = d['language_excursion']
		this_auditory = d['auditory_excursion']
		this_participants = d['participants_excursion']
		this_age = d['age_excursion']

		areas=[]

		for a in this_areas:
			areas.append(a['name_area'])

		excursions_all[d['id_facility_id']] = {
		'facility':this_facilities[0]['name_facility'],
		'areas':areas,
		'organizator': this_organizator,
		'guide':this_guide[0]['lastName_guide'],
		'occasion':this_occasion,
		'date':this_date,
		'time':this_time,
		'language':this_language,
		'auditory':this_auditory,
		'participants':this_participants,
		'age':this_age,
		}

	#return JsonResponse({'excursions':excursions_all})
	return render(request, 'schedule.html', context={'excursions':excursions_all})



@login_required
def delete_excursion(request):
	cleaner = ExcursionDelete()
	return render(request, 'ex_confirm_delete.html', context={'excursion':cleaner})

