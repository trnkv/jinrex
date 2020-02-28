from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import json
import datetime

from .models import Excursion, Area, Facility, Guide, Incharge, Chat, Message
from django.contrib.auth.models import User, Group, Permission
from .forms import SendExcursionForm, ViewExcursionForm, MessageForm

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from django.utils import timezone

import pdb


# Функция отображения для домашней страницы сайта.
# user_id = request.user.id
# users = User.objects.all().values()
# groups = Group.objects.all().values()
# permissions = Permission.objects.all().values()

def get_facility_name(facility_id):
    facility = Facility.objects.filter(id=facility_id).first()
    return facility.name


@login_required
def index(request):
    return render(request, 'base.html', context={})


@login_required
def profile(request):
    """Функция отображения профиля пользователя."""
    user_groups = []   

    for g in request.user.groups.all():
        if g.name == 'Guide':
            info_current_group = {'role':'', 'excursions':[]}
            guide = Guide.objects.get(user=request.user)       
            excursions = Excursion.objects.filter(guide=guide)
            if excursions.exists():
                info_current_group['role'] = g.name
                for ex in excursions:
                    info_current_group['excursions'].append(
                        {
                            'facility': ex.facility.name,
                            'date': ex.date,
                            'event': ex.event
                        }
                    )
                user_groups.append(info_current_group)
        if g.name == 'Incharge':
            info_current_group = {'role':'', 'excursions':[]}
            incharge = Incharge.objects.get(user=request.user)
            info_current_group['role'] = g.name
            info_current_group['excursions'].append(
                {
                    'facility': incharge.facility.name
                }
            )
            user_groups.append(info_current_group)
        if g.name == 'Organizator':
            info_current_group = {'role':'', 'excursions':[]}
            excursions = Excursion.objects.filter(organizator=request.user)
            if excursions.exists():
                for ex in excursions:
                    info_current_group['role'] = g.name
                    info_current_group['excursions'].append(
                        {
                            'facility': ex.facility.name,
                            'date': ex.date,
                            'event': ex.event
                        }
                    )
                user_groups.append(info_current_group)

    # return JsonResponse({'user_groups': user_groups})
    return render(request, 'profile.html', context={'user_groups': user_groups})


@login_required
def get_excursion_form(request):
    form = SendExcursionForm()
    print(timezone.localtime(timezone.now()))
    return render(request, 'excursion_form.html', {'form': form})


@login_required
def get_all_areas_by_facility_id(request):
    if request.method == 'POST':
        id_facility = request.POST.get('facility')
        if id_facility != '0':
            queryset_areas = Area.objects.filter(facility=id_facility)
            areas = [area.name for area in queryset_areas]
            incharges_queryset = Incharge.objects.filter(facility=id_facility)
            incharges = [incharge.user.first_name + " " + incharge.user.last_name + " (@" + incharge.user.get_username() + ")" for incharge in incharges_queryset]

            return JsonResponse({'areas': areas,
                                 'incharges': incharges})

        else:
            return JsonResponse({'result': 0})

def get_selected_areas_by_excursion_id(request):
    if request.method == 'POST':
        excursion_id = request.POST.get('excursion')
        excursion = Excursion.objects.get(id=excursion_id)
        areas_names = [area.name for area in excursion.areas.all()]
        return JsonResponse({'areas_names':areas_names})
    return HttpResponse(404)





@login_required
def send_application(request):
    if request.method == 'POST':
        form = SendExcursionForm(request.POST)

        facility = Facility.objects.get(id=request.POST.get('facility'))
        areas_ids = request.POST.getlist('areas')
        organizator = request.user
        guide_user = User.objects.get(id=request.POST.get('guide'))
        guide = Guide.objects.get(user=guide_user)
        # incharge = Incharge.objects.get(facility=facility)

        new_ex = Excursion.objects.create(
            facility=facility,
            organizator=organizator,
            guide=guide,
            incharge=None,
            event=request.POST.get('event'),
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            stop_time=request.POST.get('stop_time'),
            language=request.POST.get('language'),
            target_audience=request.POST.get('target_audience'),
            participants=request.POST.get('participants'),
        )

        new_ex.areas.set(areas_ids)
        new_ex.save()

        request.user.groups.add(Group.objects.get(name='Organizator'))

        theme = 'New excursion'
        message = 'You have received a request for a new excursion. To accept or reject it please log in to the JINRex web service.'
        from_email = 'ttrnkv75@yandex.ru'
        to_email = ['nura1ina@yandex.ru', 'trnkv13@rambler.ru']

        send_mail(theme, message, from_email, to_email, fail_silently=False)

        return render(request, 'submitted.html', context={
            'result': 'Thanks, your application is submitted! Notification of this application sent to the Guide, Incharge and Organizator.'})


@login_required
def view_excursions(request):
    def add_info_about_current_excursions(ex_queryset, result_list):
        for ex in ex_queryset:
            queryset_areas = ex.areas.all()
            info_current_excursion = {
            'id_excursion':ex.id,
            'facility':ex.facility.name,
            'areas':[area.name for area in queryset_areas],
            'date':ex.date,
            'start_time':ex.start_time,
            'stop_time':ex.stop_time,
            'confirmed_by_guide': ex.confirmed_by_guide,
            'confirmed_by_incharge': ex.confirmed_by_incharge,
            'not_held': ex.not_held
            }
            result_list.append(info_current_excursion)

    user_excursions = []
    for g in request.user.groups.all():
        if g.name == 'Guide':
            guide = Guide.objects.get(user=request.user)
            excursions_where_user_is_guide = Excursion.objects.filter(guide=guide)
            add_info_about_current_excursions(excursions_where_user_is_guide, user_excursions)
        if g.name == 'Incharge':
            incharge = Incharge.objects.get(user=request.user)
            excursions_where_user_is_incharge = Excursion.objects.filter(incharge=incharge)
            add_info_about_current_excursions(excursions_where_user_is_incharge, user_excursions)
        if g.name == 'Organizator':
            excursions_where_user_is_organizator = Excursion.objects.filter(organizator=request.user)
            add_info_about_current_excursions(excursions_where_user_is_organizator, user_excursions)

    # return JsonResponse({'user_excursions': user_excursions})

    all_excursions_queryset = Excursion.objects.all()
    all_excursions = []
    add_info_about_current_excursions(all_excursions_queryset, all_excursions)

    # return JsonResponse({'all_excursions': all_excursions})

    return render(request, 'schedule.html', context={'my_excursions': user_excursions, 'all_excursions': all_excursions})


@login_required
def get_excursion(request, id_excursion):

    # return JsonResponse({'request': request.POST.dict})

    qs_ex = Excursion.objects.get(id=id_excursion)
    excursion_areas = qs_ex.areas.all()
    incharge = None
    if qs_ex.incharge != None:
        incharge = qs_ex.incharge.user.id

    excursion_info = {
        'id': qs_ex.id,
        'facility': qs_ex.facility.id,
        'areas_names': [area.name for area in excursion_areas],
        'areas_ids': [area.id for area in excursion_areas],
        'organizator': qs_ex.organizator.id,
        'guide': qs_ex.guide.user.id,
        'incharge': incharge,
        'date': qs_ex.date,
        'start_time': qs_ex.start_time.strftime("%H:%M"),
        'stop_time': qs_ex.stop_time.strftime("%H:%M"),
        'language': qs_ex.language,
        'target_audience': qs_ex.target_audience,
        'participants': qs_ex.participants,
        'event': qs_ex.event,
        'confirmed_by_guide': qs_ex.confirmed_by_guide,
        'confirmed_by_incharge': qs_ex.confirmed_by_incharge,
        'not_held': qs_ex.not_held
    }

    # return  JsonResponse({'excursion_info': excursion_info})

    is_user_organizator = False
    is_user_guide = False
    is_user_incharge = False

    if request.user == qs_ex.organizator:
        is_user_organizator = True
    if request.user == qs_ex.guide:
        is_user_guide = True
    
    # to add an opportunity for any incharge to confirm his participation
    all_incharges_of_this_facility = Incharge.objects.filter(facility=qs_ex.facility)
    for facility_incharge in all_incharges_of_this_facility:
        if request.user == facility_incharge.user:
            is_user_incharge = True
            break

    form = ViewExcursionForm(initial=excursion_info)

    # return form.as_ul()
    # return JsonResponse({'desired_excursion':desired_excursion})

    chat = Chat.objects.filter(members__in=[request.user.id], excursion=id_excursion)
    if chat.exists():
        messages = Message.objects.filter(chat=chat.first().id).values()
        for m in messages:
            m['author'] = User.objects.get(id=m['author_id'])
        return render(request, 'excursion_info.html',
                      {
                      'excursion': excursion_info,
                      'form': form,
                      'chat': chat,
                      'messages': messages,
                      'form_message': MessageForm(),
                      'is_user_organizator':is_user_organizator,
                      'is_user_guide':is_user_guide,
                      'is_user_incharge':is_user_incharge
                      })
    else:
        chat = create_chat(
            request,
            qs_ex.organizator,
            qs_ex.incharge,
            qs_ex.guide,
            int(id_excursion))

        #return JsonResponse({'chat':chat})

        return render(request, 'excursion_info.html',
                      {
                      'excursion': excursion_info,
                      'form': form,
                      'chat': chat,
                      'messages':'none',
                      'is_user_organizator':is_user_organizator,
                      'is_user_guide':is_user_guide,
                      'is_user_incharge':is_user_incharge
                      })


    return HttpResponse(form.as_p())


def create_chat(request, organizator, incharge, guide, id_excursion):
    if request.user != organizator and request.user != incharge and request.user != guide:
        return {'error': 'You can not view this chat because you are not in members of this excursion.'}
    else:
        chat = Chat.objects.create(excursion=Excursion.objects.get(id=id_excursion))
        chat.members.add(organizator)
        chat.members.add(incharge)
        chat.members.add(guide)
        chat = Chat.objects.filter(excursion=id_excursion).values()
        return [v for v in chat]
    #return redirect(get_excursion(id_excursion))


@login_required
def change_confirmed(request, id_excursion):
    qs_ex = Excursion.objects.get(id=id_excursion)

    current_guide = qs_ex.guide

    current_incharge = qs_ex.incharge

    if current_incharge != None:
        if request.user == current_incharge.user:
            Excursion.objects.filter(id=id_excursion).update(confirmed_by_incharge=True)
            return HttpResponse(status=204)
    else:
        created_incharge = Incharge.objects.create(facility=qs_ex.facility, user=request.user)
        request.user.groups.add(Group.objects.get(name='Incharge'))
        Excursion.objects.filter(id=id_excursion).update(incharge=created_incharge, confirmed_by_incharge=True)
        chat = Chat.objects.get(excursion=id_excursion)
        chat.members.add(request.user)
        return HttpResponse(status=204)

    if request.user == current_guide.user:
        Excursion.objects.filter(id=id_excursion).update(confirmed_by_guide=True)
        return HttpResponse(status=204)

    return HttpResponse(status=500)



@login_required
def change_excursion(request, id_excursion):

    # g = Guide.objects.all().values('id')
    # return JsonResponse({'guides':[v for v in g]})

    # return JsonResponse({'request':request.POST.dict()})

    # form = ViewExcursionForm(request.POST)

    # if form.is_valid():
    current_excursion = Excursion.objects.get(id=id_excursion)

    # return JsonResponse({'desired_excursion': desired_excursion})

    current_guide = current_excursion.guide    
    new_guide_user = User.objects.get(id=request.POST.get('guide'))
    new_guide = Guide.objects.get(user=new_guide_user)

    # if Facility has not been changed
    old_incharge = current_excursion.incharge
    incharge = None
    if request.POST.get('incharge') != '0':
        incharge = old_incharge

    new_ex = Excursion.objects.filter(id=id_excursion).update(
        id=id_excursion,
        facility=Facility.objects.get(id=request.POST.get('facility')),
        incharge = incharge,
        guide=new_guide,
        event=request.POST.get('event'),
        date=request.POST.get('date'),
        start_time=request.POST.get('start_time'),
        stop_time=request.POST.get('stop_time'),
        language=request.POST.get('language'),
        target_audience=request.POST.get('target_audience'),
        participants=request.POST.get('participants'),
        confirmed_by_guide=False,
        confirmed_by_incharge=False,
        not_held=False)


    new_ex = Excursion.objects.get(id=id_excursion)


    new_ex.areas.set(request.POST.getlist('areas'))
    new_ex.save()

    # incharge = [v for v in User.objects.filter(id=request.POST.get('incharge')).values('id')][0]['id']
    # guide = [v for v in User.objects.filter(id=request.POST.get('guide')).values('id')][0]['id']

    # new_guide_queryset = Guide.objects.filter(id=request.POST.get('guide')).values('user')
    # new_guide = [val for val in new_guide_queryset]
    # user_new_guide = User.objects.get(id=new_guide[0]['user'])

    # Updating Chat members
    chat = Chat.objects.get(excursion=id_excursion)
    if (current_guide.user != new_guide_user):
        chat.members.remove(current_guide.user)
        chat.members.add(new_guide_user)
    if incharge == None and old_incharge != None:
        chat.members.remove(old_incharge.user)


    return render(request, 'submitted.html', context={'result': 'The excursion is updated!'})
    # else: return render(request, 'submitted.html', context={'result': 'Mistakes were made in filling out the form. Please correct the errors and resend again.'})


def send_message(request, id_excursion, chat_id):
    form = MessageForm(data=request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.chat = Chat.objects.get(excursion=id_excursion)
        message.author = request.user
        message.save()

    return HttpResponseRedirect('/../jinrex/schedule/get_excursion/'+id_excursion)


def mark_as_not_held(request, id_excursion):
    Excursion.objects.filter(id=id_excursion).update(not_held=True)
    return HttpResponse(status=204)


def view_facilities_attendace(request):
    all_excursions = Excursion.objects.filter(not_held = False).values('facility', 'date')
    all_excursions = [val for val in all_excursions if val in all_excursions]
    for ex in all_excursions:
        ex['date'] = str(ex['date'])[:4]
        ex['facility'] = get_facility_name(ex['facility'])
    # return JsonResponse({'excursions':all_excursions})
    return render(request, 'facilities_attendance.html', context={'excursions':all_excursions})

def view_areas_attendace(request):
    all_excursions = Excursion.objects.filter(not_held = False).values('areas', 'date')
    all_excursions = [val for val in all_excursions if val in all_excursions]
    for ex in all_excursions:
        ex['areas'] = [val for val in Area.objects.filter(id=ex['areas']).values('name')][0]['name']
        ex['date'] = str(ex['date'])[:4]
    # return JsonResponse({'excursions':all_excursions})
    return render(request, 'areas_attendance.html', context={'excursions':all_excursions})


def view_guide_statistics(request):
    return render(request, 'guides_statistics.html', {})

def get_all_facilities():
    all_excursions = Excursion.objects.filter(not_held = False)
    all_facilities = []

    for ex in all_excursions:
        all_facilities.append(ex.facility.name)
    all_facilities = sorted(list(set(all_facilities)), reverse=True)
    return all_facilities

def get_all_guides():
    all_excursions = Excursion.objects.filter(not_held = False)
    all_guides = []

    for ex in all_excursions:
        all_guides.append(ex.guide)
    all_guides = list(set(all_guides))
    return all_guides



def get_guide_statistics(request):
    all_excursions = Excursion.objects.filter(not_held = False)
    #all_excursions = [val for val in all_excursions if val in all_excursions]

    guides = {}
    result_info = []
    all_facilities = get_all_facilities()
    all_guides = get_all_guides()
    facilities = []

    for guide in all_guides:
        result_info.append(dict(name=guide.user.get_username(), facilities={}))

    for ex in all_excursions:
        for d in result_info:
            if d['name'] == ex.guide.user.get_username():
                if ex.facility.name in d['facilities']:
                    d['facilities'][ex.facility.name] += 1
                else:
                    d['facilities'][ex.facility.name] = 1
                    for other in all_facilities:
                        if ex.facility.name != other:
                            d['facilities'][other] = 0
                break
    return JsonResponse({'all_facilities':all_facilities, 'guide_statistics':result_info})
    # return render(request, 'guides_statistics.html', context={'all_facilities':json.dumps(all_facilities),'guides': json.dumps(result_info)})


def view_calendar(request):
    return render(request, 'calendar.html', {})


def get_excursions_to_calendar(request):
    # return JsonResponse({'all_guides':list(Guide.objects.values())})
    # return json.dumps(list(Guide.objects.all()))
    calendar = []
    all_excursions = Excursion.objects.all()
    for ex in all_excursions:
        start = ex.date.strftime("%Y, %m, %d") + ', ' + ex.start_time.strftime("%H, %M")
        end = ex.date.strftime("%Y, %m, %d") + ', ' + ex.stop_time.strftime("%H, %M")
        print(start)
        calendar.append(
            {
                'title': ex.facility.name + ', ' + ex.event,
                'start': start,
                'end': end
            }
        )
    return JsonResponse({'calendar':calendar})
    # return render(request, 'calendar.html', {'calendar':json.dumps(calendar)})
