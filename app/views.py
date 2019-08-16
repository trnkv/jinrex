from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import JsonResponse
import json

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
	form = ExcursionForm()
	return render(request, 'excursion_form.html', {'form':form})

@login_required
def get_excursion(request, id_excursion):
	queryset_desired_excursion = Excursion.objects.filter(id_excursion=id_excursion).values()
	desired_excursion = [val for val in queryset_desired_excursion if val in queryset_desired_excursion]

	queryset_facility = Facility.objects.filter(id_facility=desired_excursion[0]['id_facility_id']).values('name_facility')
	facility = [val for val in queryset_facility if val in queryset_facility]

	desired_excursion[0]['name_facility'] = facility[0]['name_facility']

	excursion = Excursion.objects.get(id_excursion=desired_excursion[0]['id_excursion'])
	queryset_areas = excursion.id_area.all().values('name_area')
	list_areas = [val for val in queryset_areas if val in queryset_areas]

	areas = []
	for area in list_areas:
		areas.append(area['name_area'])

	desired_excursion[0]['areas'] = areas

	this_guide = list(Guide.objects.filter(id_guide=desired_excursion[0]['id_guide_id']).values('lastName_guide'))
	desired_excursion[0]['lastName_guide'] = this_guide[0]['lastName_guide']

	form = ExcursionForm(desired_excursion[0])

	return render(request, 'excursion_info.html', {'desired_excursion':desired_excursion, 'form':form})

@login_required
def send_excursion_form(request):
	if request.method == 'POST':
		form = ExcursionForm(request.POST)
		if form.is_valid():
			print('POST request valid. Looks like you are sending some data to the server')

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
			new_ex.save()

			return render(request, 'submitted.html', context={})


@login_required
def submitted(request):
    """Функция отображения успешной отправки заявки на экскурсию."""
    return render(request, 'submitted_ex_blank.html', context={})

@login_required
def view_excursions(request):
	excursions = Excursion.objects.all().values()
	excursions = [val for val in excursions if val in excursions]

	for d in excursions:
		
		this_facilities = list(Facility.objects.filter(id_facility=d['id_facility_id']).values('name_facility'))

		excursion = Excursion.objects.get(id_excursion=d['id_excursion'])
		queryset = excursion.id_area.all().values('name_area')
		areas = [val for val in queryset if val in queryset]

		ar = []
		for area in areas:
				ar.append(area['name_area'])

		this_guide = list(Guide.objects.filter(id_guide=d['id_guide_id']).values('lastName_guide'))

		d['areas'] = ar
		d['id_facility_id'] = this_facilities[0]['name_facility']
		d['id_guide_id'] = this_guide[0]['lastName_guide']

	json_data = json.dumps(excursions, indent=4, sort_keys=False, default=str)

	return render(request, 'schedule.html', context={'excursions':excursions})


@login_required
def update_excursion(request):
	excursion = Excursion.objects.all()
	if request.POST:
		name_organizator = request.POST['name_organizator']
		occasion_excursion = request.POST['occasion_excursion']
		time_period_excursion = request.POST['time_period_excursion']
		language_excursion = request.POST['language_excursion']
		auditory_excursion = request.POST['auditory_excursion']
		participants_excursion = request.POST['participants_excursion']
		age_excursion = request.POST['age_excursion']

		edited_field = excursion.get(id_facility=field)
		edited_node.comment = request.POST.get('comment')
		
		edited_node.save()

	# render template with nodes
	return render(request, 'submitted_ex_update.html', {})