from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import json

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
        info = {'group':'', 'excursions':[]}
        if g.name == 'Guide':
            info["group"] = g.name
            guide_user = User.objects.get(id=request.user.id)
            guide = Guide.objects.get(user=guide_user)
            excursions = Excursion.objects.filter(guide=guide)
            if excursions.exists():
                for ex in excursions:
                    facility_name = ex.facility.name
                    date = ex.date
                    event = ex.event
                    info["excursions"].append(
                    {
                        'facility': facility_name,
                        'date': date.strftime("%d.%m.%Y"),
                        'event': event
                    })
            else:
                info["excursions"].append("Now you haven't any excursion.")

        if g.name == 'Incharge':
            info["group"] = g.name
            incharge_user = User.objects.get(id=request.user.id)
            incharge = Incharge.objects.filter(user=incharge_user).first()
            facility_name = incharge.facility.name
            info["excursions"].append(facility_name)

        if g.name == 'Organizator':
            info["group"] = g.name
            excursions = Excursion.objects.filter(organizator=request.user)
            for ex in excursions:
                facility_name = ex.facility.name
                date = ex.date
                event = ex.event
                info["excursions"].append(
                {
                    'facility': facility_name,
                    'date': date.strftime("%d.%m.%Y"),
                    'event': event
                })
        user_groups.append(info)

    return JsonResponse({'user_groups': user_groups})
    # return render(request, 'profile.html', context={'user_groups': json.dumps(user_groups)})


# return JsonResponse({'user_groups':user_groups})


@login_required
def get_excursion_form(request):
    form = SendExcursionForm()
    print(timezone.localtime(timezone.now()))
    return render(request, 'excursion_form.html', {'form': form})


@login_required
def get_areas(request):
    if request.method == 'POST':
        id_facility = request.POST.get('facility')
        if id_facility != '0':
            list_of_dict_areas = list(Area.objects.filter(facility=id_facility).values('name'))
            areas = []
            for d in list_of_dict_areas:
                areas.append(d['name'])

            incharge = Incharge.objects.filter(facility=id_facility).values('user_id')
            incharge_id = User.objects.filter(pk=incharge[0]['user_id']).values('id')[0]['id']
            incharge_first_name = User.objects.filter(pk=incharge[0]['user_id']).values('first_name')[0]['first_name']
            incharge_last_name = User.objects.filter(pk=incharge[0]['user_id']).values('last_name')[0]['last_name']
            incharge_username = User.objects.filter(pk=incharge[0]['user_id']).values('username')[0]['username']

            return JsonResponse({'areas': areas,
                                 'id_incharge': incharge_id,
                                 'info_incharge': incharge_first_name + " " + incharge_last_name + " (@" + incharge_username + ")"})

        else:
            return JsonResponse({'result': 0})


@login_required
def send_excursion_form(request):
    if request.method == 'POST':

        form = SendExcursionForm(request.POST)

        # if form.is_valid():
        facility_id = Facility.objects.get(id=request.POST.get('facility'))

        areas_ids = request.POST.getlist('areas')

        organizator = request.user

        guide_user = User.objects.get(id=request.POST.get('guide'))
        guide = Guide.objects.get(user=guide_user)

        incharge = Incharge.objects.get(facility=request.POST.get('facility'))
        incharge_id = Incharge.objects.filter(facility=request.POST.get('facility')).values('id')[0]['id']
        incharge_user = User.objects.get(id=incharge_id)

        new_ex = Excursion.objects.create(
            facility=facility_id,
            organizator=organizator,
            guide=guide,
            incharge=incharge,
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

        request.user.groups.add(Group.objects.filter(name='Organizator').values('id')[0]['id'])

        theme = 'New excursion'
        message = 'You have received a request for a new excursion. To accept or reject it please log in to the JINRex web service.'
        from_email = 'ttrnkv75@yandex.ru'
        to_email = ['nura1ina@yandex.ru', 'trnkv13@rambler.ru']

        send_mail(theme, message, from_email, to_email, fail_silently=False)

        return render(request, 'submitted.html', context={
            'result': 'Thanks, your application is submitted! Notification of this application sent to the Guide, Incharge and Organizator.'})


@login_required
def view_excursions(request):
    current_user = request.user
    current_user_id = request.user.id

    user_excursions = []

    for g in request.user.groups.all().values():
        # g - ЭТО dict
        if g['name'] == 'Guide':
            guide_user = User.objects.get(id=current_user_id)
            guide = Guide.objects.get(user=guide_user)
            excursions_where_user_is_guide = Excursion.objects.filter(guide=guide).values('id', 'confirmed_by_guide', 'confirmed_by_incharge', 'facility', 'date', 'start_time', 'stop_time', 'not_held')
            excursions_where_user_is_guide = [val for val in excursions_where_user_is_guide if val in excursions_where_user_is_guide]
            for ex in excursions_where_user_is_guide:
                excursion = Excursion.objects.get(id=ex['id'])
                queryset = excursion.areas.all().values('name')
                ex['facility'] = Facility.objects.filter(id=ex['facility']).values('name')[0]['name']
                areas = [val for val in queryset if val in queryset]

                ar = []
                for area in areas:
                    ar.append(area['name'])
                ex['areas'] = ar
                user_excursions.append(ex)

        if g['name'] == 'Incharge':
            incharge_user = User.objects.get(id=current_user_id)
            incharge = Incharge.objects.get(user=incharge_user)
            excursions_where_user_is_incharge = Excursion.objects.filter(incharge=incharge).values('id', 'confirmed_by_guide', 'confirmed_by_incharge', 'facility', 'date', 'start_time', 'stop_time', 'not_held')
            excursions_where_user_is_incharge = [val for val in excursions_where_user_is_incharge if val in excursions_where_user_is_incharge]
            for ex in excursions_where_user_is_incharge:
                excursion = Excursion.objects.get(id=ex['id'])
                queryset = excursion.areas.all().values('name')
                ex['facility'] = Facility.objects.filter(id=ex['facility']).values('name')[0]['name']
                areas = [val for val in queryset if val in queryset]

                ar = []
                for area in areas:
                    ar.append(area['name'])
                ex['areas'] = ar
                user_excursions.append(ex)

        if g['name'] == 'Organizator':
            excursions_where_user_is_organizator = Excursion.objects.filter(organizator=current_user).values('id', 'confirmed_by_guide', 'confirmed_by_incharge', 'facility', 'date', 'start_time', 'stop_time', 'not_held')
            excursions_where_user_is_organizator = [val for val in excursions_where_user_is_organizator if val in excursions_where_user_is_organizator]
            for ex in excursions_where_user_is_organizator:
                excursion = Excursion.objects.get(id=ex['id'])
                queryset = excursion.areas.all().values('name')
                ex['facility'] = Facility.objects.filter(id=ex['facility']).values('name')[0]['name']
                areas = [val for val in queryset if val in queryset]

                ar = []
                for area in areas:
                    ar.append(area['name'])
                ex['areas'] = ar
                user_excursions.append(ex)

    # return JsonResponse({'user_excursions': user_excursions})
    #return user_excursions

    all_excursions = Excursion.objects.all().values()
    all_excursions = [val for val in all_excursions if val in all_excursions]

    for d in all_excursions:
        this_facilities = list(Facility.objects.filter(id=d['facility_id']).values('name'))
        excursion = Excursion.objects.get(id=d['id'])
        queryset = excursion.areas.all().values('name')
        areas = [val for val in queryset if val in queryset]

        ar = []
        for area in areas:
            ar.append(area['name'])

        d['areas'] = ar
        d['facility'] = this_facilities[0]['name']

    return render(request, 'schedule.html', context={'my_excursions': user_excursions, 'all_excursions': all_excursions})


@login_required
def get_excursion(request, id_excursion):

    # return JsonResponse({'request': request.POST.dict})

    queryset_desired_excursion = Excursion.objects.filter(id=id_excursion).values()
    desired_excursion = [val for val in queryset_desired_excursion if val in queryset_desired_excursion]

    desired_excursion[0]['facility'] = get_facility_name(desired_excursion[0]['facility_id'])

    excursion = Excursion.objects.get(id=desired_excursion[0]['id'])
    queryset_areas_names = excursion.areas.all().values('name')
    queryset_areas_ids = excursion.areas.all().values('id')

    list_areas_names = [val for val in queryset_areas_names if val in queryset_areas_names]
    areas_names = []
    for area in list_areas_names:
        areas_names.append(area['name'])
    desired_excursion[0]['areas_names'] = areas_names

    list_areas_ids = [val for val in queryset_areas_ids if val in queryset_areas_ids]
    areas_ids = []
    for area in list_areas_ids:
        areas_ids.append(area['id'])

    desired_excursion[0]['areas_ids'] = areas_ids

    user_organizator = list(User.objects.filter(id=desired_excursion[0]['organizator_id']))
    desired_excursion[0]['organizator'] = user_organizator[0]

    guide = list(Guide.objects.filter(id=desired_excursion[0]['guide_id']).values('user'))
    user_guide = User.objects.get(id=guide[0]['user'])
    desired_excursion[0]['guide'] = user_guide

    incharge = list(Incharge.objects.filter(facility=desired_excursion[0]['facility_id']).values('user'))
    user_incharge = User.objects.get(id=incharge[0]['user'])
    desired_excursion[0]['incharge'] = user_incharge

    # return  JsonResponse({'desired_excursion': desired_excursion})

    is_user_organizator = False
    is_user_guide = False
    is_user_incharge = False

    # if request.user == user_guide and desired_excursion[0]['confirmed_by_guide']:
    #     confirmed_by_guide = True
    # if request.user == user_incharge and desired_excursion[0]['confirmed_by_incharge']:
    #    confirmed_by_incharge = True
    # if request.user == desired_excursion[0]['organizator'] and desired_excursion[0]['confirmed_guide'] and desired_excursion[0]['confirmed_incharge']:
    #     confirmed = True


    if request.user == desired_excursion[0]['organizator']:
        is_user_organizator = True

    if request.user == desired_excursion[0]['guide']:
        is_user_guide = True

    if request.user == desired_excursion[0]['incharge']:
        is_user_incharge = True

    # return JsonResponse({'ex':desired_excursion[0]})
    #return JsonResponse({'incharge': desired_excursion[0]['incharge']})

    form = ViewExcursionForm(initial={
        'facility': desired_excursion[0]['facility_id'],
        'areas': queryset_areas_ids,
        'organizator': desired_excursion[0]['organizator'],
        'guide': desired_excursion[0]['guide'],
        'incharge': desired_excursion[0]['incharge'],
        'event': desired_excursion[0]['event'],
        'date': desired_excursion[0]['date'],
        'start_time': desired_excursion[0]['start_time'],
        'stop_time': desired_excursion[0]['stop_time'],
        'language': desired_excursion[0]['language'],
        'target_audience': desired_excursion[0]['target_audience'],
        'participants': desired_excursion[0]['participants'],
    })

    # return JsonResponse({'desired_excursion':desired_excursion})

    chat = Chat.objects.filter(members__in=[request.user.id], excursion=id_excursion).values()
    if len(chat) != 0:
        messages = Message.objects.filter(chat=chat[0]['id']).values()
        for m in messages:
            m['author'] = User.objects.get(id=m['author_id'])
        # return JsonResponse({
        #               'desired_excursion': desired_excursion[0],
        #               'form': form,
        #               'chat': chat,
        #               'messages': messages,
        #               'form_message': MessageForm()
        #               })
        return render(request, 'excursion_info.html',
                      {
                      'desired_excursion': desired_excursion[0],
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
            desired_excursion[0]['organizator'],
            desired_excursion[0]['incharge'],
            desired_excursion[0]['guide'],
            int(id_excursion))

        #return JsonResponse({'chat':chat})

        return render(request, 'excursion_info.html',
                      {
                      'desired_excursion': desired_excursion[0],
                      # 'confirmed_guide': desired_excursion[0]['confirmed_guide'],
                      # 'confirmed_incharge': desired_excursion[0]['confirmed_incharge'],
                      'form': form,
                      'chat': chat,
                      'messages':'none',
                      'is_user_organizator':is_user_organizator,
                      'is_user_guide':is_user_guide,
                      'is_user_incharge':is_user_incharge
                      })


# return HttpResponse(form.as_p())


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
    queryset_excursion = Excursion.objects.filter(id=id_excursion).values()
    excursion = [val for val in queryset_excursion]

    this_guide = list(Guide.objects.filter(id=excursion[0]['guide_id']).values('user'))
    user_guide = User.objects.get(id=this_guide[0]['user'])

    this_incharge = list(Incharge.objects.filter(facility=excursion[0]['facility_id']).values('user'))
    user_incharge = User.objects.get(id=this_incharge[0]['user'])

    if request.user == user_incharge:
        Excursion.objects.filter(id=id_excursion).update(confirmed_by_incharge=True)
        return HttpResponse(status=204)

    if request.user == user_guide:
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
    queryset_desired_excursion = Excursion.objects.filter(id=id_excursion).values()
    desired_excursion = [val for val in queryset_desired_excursion if val in queryset_desired_excursion]

    # return JsonResponse({'desired_excursion': desired_excursion})

    this_guide = list(Guide.objects.filter(facility=desired_excursion[0]['facility_id']).values('user'))
    user_guide = User.objects.get(id=this_guide[0]['user'])

    new_guide_user = User.objects.get(id=request.POST.get('guide'))
    new_guide = Guide.objects.get(user=new_guide_user)


    new_ex = Excursion.objects.filter(id=id_excursion).update(
        id=id_excursion,
        facility=Facility.objects.get(id=request.POST.get('facility')),
        guide=new_guide,
        event=request.POST.get('event'),
        date=request.POST.get('date'),
        start_time=request.POST.get('start_time'),
        stop_time=request.POST.get('stop_time'),
        language=request.POST.get('language'),
        target_audience=request.POST.get('target_audience'),
        participants=request.POST.get('participants'),
        confirmed_guide=False,
        confirmed_incharge=False,
        not_held=False)


    new_ex = Excursion.objects.get(id=id_excursion)


    new_ex.areas.set(request.POST.getlist('areas'))
    new_ex.save()

    # incharge = [v for v in User.objects.filter(id=request.POST.get('incharge')).values('id')][0]['id']
    # guide = [v for v in User.objects.filter(id=request.POST.get('guide')).values('id')][0]['id']

    # new_guide_queryset = Guide.objects.filter(id=request.POST.get('guide')).values('user')
    # new_guide = [val for val in new_guide_queryset]
    # user_new_guide = User.objects.get(id=new_guide[0]['user'])

    if (user_guide != new_guide_user):
        chat = Chat.objects.get(excursion=id_excursion)
        chat.members.remove(user_guide)
        chat.members.add(new_guide_user)

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
    all_excursions = Excursion.objects.filter(not_held = False)
    #all_excursions = [val for val in all_excursions if val in all_excursions]

    guides = {}
    result_info = []
    all_facilities = []
    all_guides = []
    facilities = []

    for ex in all_excursions:
        all_facilities.append(ex.facility.name)
        all_guides.append(ex.guide)
    all_facilities = list(set(all_facilities))
    all_guides = list(set(all_guides))

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
    return render(request, 'guides_statistics.html', context={'all_facilities':json.dumps(all_facilities),'guides': json.dumps(result_info)})


def view_calendar(request):
    # return JsonResponse({'all_guides':list(Guide.objects.values())})
    # return json.dumps(list(Guide.objects.all()))
    return render(request, 'calendar.html', {'all_guides':json.dumps(list(Guide.objects.values()))})
