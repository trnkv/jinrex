from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json

from .models import Excursion, Area, Facility, Incharge, Chat, Message
from django.contrib.auth.models import User, Group, Permission
from .forms import SendExcursionForm, ViewExcursionForm, MessageForm

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail


# Функция отображения для домашней страницы сайта.
# user_id = request.user.id
# users = User.objects.all().values()
# groups = Group.objects.all().values()
# permissions = Permission.objects.all().values()


@login_required
def index(request):
    return render(request, 'index.html', context={})


@login_required
def profile(request, user_id):
    """Функция отображения профиля пользователя."""
    user_groups = []

    username = request.user.username
    print(username)

    for g in request.user.groups.all():
        user_groups.append(g)

    # group_organizator = Group.objects.get(name='Organizator')
    # group_guide = Group.objects.get(name='Guide')
    # group_incharge = Group.objects.get(name='Incharge')

    # users_o = group_organizator.user_set.filter(username=username)
    # users_g = group_guide.user_set.filter(username=username)
    # users_i = group_incharge.user_set.filter(username=username)

    # users = [users_o, users_g, users_i]
    # for u in users:
    #   if len(u) != 0:
    #       if users.index(u) == 0:
    #           user_groups.append('Organizator')
    #       if users.index(u) == 1:
    #           user_groups.append('Guide')
    #       if users.index(u) == 2:
    #           user_groups.append('Incharge')

    return render(request, 'profile.html', context={'user_groups': user_groups})


# return JsonResponse({'user_groups':user_groups})


@login_required
def get_excursion_form(request):
    form = SendExcursionForm()
    return render(request, 'excursion_form.html', {'form': form})


@login_required
def get_areas(request):
    if request.method == 'POST':
        id_facility = request.POST.get('id_facility')
        if id_facility != '0':
            print('true')
            list_of_dict_areas = list(Area.objects.filter(id_facility=id_facility).values('name_area'))
            areas = []
            for d in list_of_dict_areas:
                areas.append(d['name_area'])

            incharge = Incharge.objects.filter(id_facility=id_facility).values('user_id')
            incharge_id = User.objects.filter(pk=incharge[0]['user_id']).values('id')[0]['id']
            incharge_first_name = User.objects.filter(pk=incharge[0]['user_id']).values('first_name')[0]['first_name']
            incharge_last_name = User.objects.filter(pk=incharge[0]['user_id']).values('last_name')[0]['last_name']
            incharge_username = User.objects.filter(pk=incharge[0]['user_id']).values('username')[0]['username']

            return JsonResponse({'areas': areas,
                                 'id_incharge': incharge_id,
                                 'info_incharge': incharge_first_name + " " + incharge_last_name + " (@" + incharge_username + ")"})

        else:
            print('false')
            return JsonResponse({'result': 0})

    # return render_to_response('excursion_form.html', {'areas': areas})


@login_required
def send_excursion_form(request):
    if request.method == 'POST':

        form = SendExcursionForm(request.POST)

        if form.is_valid():
            facility_id = Facility.objects.get(id_facility=request.POST.get('facility'))

            areas_ids = request.POST.getlist('areas')

            organizator = request.user

            guide = User.objects.get(id=request.POST.get('guide'))

            incharge = Incharge.objects.filter(id_facility=request.POST.get('facility')).values('user')[0]['user']
            incharge_user = User.objects.get(id=incharge)

            new_ex = Excursion.objects.create(
                facility=facility_id,
                organizator=organizator,
                guide=guide,
                incharge=incharge_user,
                occasion_excursion=request.POST.get('occasion_excursion'),
                date_excursion=request.POST.get('date_excursion'),
                time_period_excursion=request.POST.get('time_period_excursion'),
                language_excursion=request.POST.get('language_excursion'),
                auditory_excursion=request.POST.get('auditory_excursion'),
                participants_excursion=request.POST.get('participants_excursion'),
                age_excursion=request.POST.get('age_excursion'))

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
    excursions = Excursion.objects.all().values()
    excursions = [val for val in excursions if val in excursions]

    for d in excursions:

        this_facilities = list(Facility.objects.filter(id_facility=d['facility_id']).values('name_facility'))

        excursion = Excursion.objects.get(id_excursion=d['id_excursion'])
        queryset = excursion.areas.all().values('name_area')
        areas = [val for val in queryset if val in queryset]

        ar = []
        for area in areas:
            ar.append(area['name_area'])

        d['areas'] = ar
        d['facility_id'] = this_facilities[0]['name_facility']

    return render(request, 'schedule.html', context={'excursions': excursions})


@login_required
def get_excursion(request, id_excursion):
    queryset_desired_excursion = Excursion.objects.filter(id_excursion=id_excursion).values()
    desired_excursion = [val for val in queryset_desired_excursion if val in queryset_desired_excursion]

    queryset_facility = Facility.objects.filter(id_facility=desired_excursion[0]['facility_id']).values('name_facility')
    facility = [val for val in queryset_facility if val in queryset_facility]

    desired_excursion[0]['name_facility'] = facility[0]['name_facility']

    excursion = Excursion.objects.get(id_excursion=desired_excursion[0]['id_excursion'])
    queryset_areas_names = excursion.areas.all().values('name_area')
    queryset_areas_ids = excursion.areas.all().values('id_area')

    list_areas_names = [val for val in queryset_areas_names if val in queryset_areas_names]
    areas_names = []
    for area in list_areas_names:
        areas_names.append(area['name_area'])

    desired_excursion[0]['areas_names'] = areas_names

    list_areas_ids = [val for val in queryset_areas_ids if val in queryset_areas_ids]
    areas_ids = []
    for area in list_areas_ids:
        areas_ids.append(area['id_area'])

    desired_excursion[0]['areas_ids'] = areas_ids

    this_organizator = list(User.objects.filter(id=desired_excursion[0]['organizator_id']))
    desired_excursion[0]['organizator'] = this_organizator[0]

    this_guide = list(User.objects.filter(id=desired_excursion[0]['guide_id']))
    desired_excursion[0]['guide'] = this_guide[0]

    this_incharge = list(Incharge.objects.filter(id_facility=desired_excursion[0]['facility_id']).values('user'))
    user_incharge = User.objects.get(id=this_incharge[0]['user'])
    desired_excursion[0]['incharge'] = user_incharge

    confirmed = False
    can_edit_form = False

    if request.user == this_guide[0] and desired_excursion[0]['confirmed_guide']:
        confirmed = True
    if request.user == user_incharge and desired_excursion[0]['confirmed_incharge']:
        confirmed = True
    if request.user == this_organizator[0] and desired_excursion[0]['confirmed_guide'] and desired_excursion[0]['confirmed_incharge']:
        confirmed = True


    if request.user == this_organizator[0]:
        can_edit_form = True

    desired_excursion[0]['is_confirmed'] = confirmed

    #return JsonResponse({'ex':desired_excursion[0]})
    #return JsonResponse({'incharge': desired_excursion[0]['incharge']})

    form = ViewExcursionForm(initial={
        'facility': desired_excursion[0]['facility_id'],
        'areas': queryset_areas_ids,
        'organizator': desired_excursion[0]['organizator'],
        'guide': desired_excursion[0]['guide'],
        'incharge': desired_excursion[0]['incharge'],
        'occasion_excursion': desired_excursion[0]['occasion_excursion'],
        'date_excursion': desired_excursion[0]['date_excursion'],
        'time_period_excursion': desired_excursion[0]['time_period_excursion'],
        'language_excursion': desired_excursion[0]['language_excursion'],
        'auditory_excursion': desired_excursion[0]['auditory_excursion'],
        'participants_excursion': desired_excursion[0]['participants_excursion'],
        'age_excursion': desired_excursion[0]['age_excursion'],
    })

    chat = Chat.objects.filter(members__in=[request.user.id], excursion=id_excursion).values()
    if len(chat) != 0:
        messages = Message.objects.filter(chat=chat[0]['id']).values()
        for m in messages:
            m['author'] = User.objects.get(id=m['author_id'])
        return render(request, 'excursion_info.html',
                      {
                      'desired_excursion': desired_excursion[0],
                      'form': form,
                      'chat': chat,
                      'messages': messages,
                      'form_message': MessageForm(),
                      'user_can_edit_form':can_edit_form
                      })
    else:
        chat = create_chat(
            request,
            desired_excursion[0]['organizator_id'],
            desired_excursion[0]['incharge_id'],
            desired_excursion[0]['guide_id'],
            int(id_excursion))

        #return JsonResponse({'chat':chat})

        return render(request, 'excursion_info.html',
                      {
                      'desired_excursion': desired_excursion[0],
                      'confirmed_guide': desired_excursion[0]['confirmed_guide'],
                      'confirmed_incharge': desired_excursion[0]['confirmed_incharge'],
                      'form': form,
                      'chat': chat,
                      'messages':'none',
                      'user_can_edit_form':can_edit_form
                      })


# return HttpResponse(form.as_p())


def create_chat(request, organizator, incharge, guide, id_excursion):
    if request.user.id != organizator and request.user.id != incharge and request.user.id != guide:
        return {'error': 'You can not view this chat because you are not in members of this excursion.'}
    else:
        chat = Chat.objects.create(excursion_id=id_excursion)
        chat.members.add(organizator)
        chat.members.add(incharge)
        chat.members.add(guide)
        chat = Chat.objects.filter(excursion_id=id_excursion).values()
        return [v for v in chat]
    #return redirect(get_excursion(id_excursion))


@login_required
def change_confirmed(request, id_excursion1):
    queryset_excursion = Excursion.objects.filter(id_excursion=id_excursion1).values()
    excursion = [val for val in queryset_excursion]

    user_guide = list(User.objects.filter(id=excursion[0]['guide_id']))[0]
    this_incharge = list(Incharge.objects.filter(id_facility=excursion[0]['facility_id']).values('user'))
    user_incharge = User.objects.get(id=this_incharge[0]['user'])
    
    if request.user == user_incharge:
        Excursion.objects.filter(id_excursion=id_excursion1).update(confirmed_incharge=True)

    if request.user == user_guide:
        Excursion.objects.filter(id_excursion=id_excursion1).update(confirmed_guide=True)
    
    return HttpResponse(status=204)



@login_required
def change_excursion(request, id_excursion1, id_excursion2):

    # return JsonResponse({'request':request.POST.dict()})

    # form = ViewExcursionForm(request.POST)

    # if form.is_valid():
    queryset_desired_excursion = Excursion.objects.filter(id_excursion=id_excursion2).values()
    desired_excursion = [val for val in queryset_desired_excursion if val in queryset_desired_excursion]

    user_incharge = list(User.objects.filter(id=request.POST.get('incharge')))[0]
    user_guide = User.objects.get(id=request.POST.get('guide'))
    #user_incharge = list(User.objects.filter(id=desired_excursion[0]['incharge_id']))[0]

    new_ex = Excursion.objects.filter(id_excursion=id_excursion2).update(
        id_excursion=id_excursion2,
        facility=Facility.objects.get(id_facility=request.POST.get('facility')),
        guide=user_guide,
        incharge=user_incharge,
        occasion_excursion=request.POST.get('occasion_excursion'),
        date_excursion=request.POST.get('date_excursion'),
        time_period_excursion=request.POST.get('time_period_excursion'),
        language_excursion=request.POST.get('language_excursion'),
        auditory_excursion=request.POST.get('auditory_excursion'),
        participants_excursion=request.POST.get('participants_excursion'),
        age_excursion=request.POST.get('age_excursion'),
        confirmed_guide=False,
        confirmed_incharge=False)

    new_ex = Excursion.objects.get(id_excursion=id_excursion2)


    new_ex.areas.set(request.POST.getlist('areas'))
    new_ex.save()

    incharge = [v for v in User.objects.filter(id=request.POST.get('incharge')).values('id')][0]['id']
    guide = [v for v in User.objects.filter(id=request.POST.get('guide')).values('id')][0]['id']

    if (desired_excursion[0]['incharge_id'] != user_incharge or desired_excursion[0]['guide_id'] != user_guide):
        chat = Chat.objects.get(excursion_id=id_excursion2)
        if desired_excursion[0]['incharge_id'] != user_incharge:
            chat.members.remove(desired_excursion[0]['incharge_id'])
            chat.members.add(incharge)
        elif desired_excursion[0]['guide_id'] != user_guide:
            chat.members.remove(desired_excursion[0]['guide_id'])
            chat.members.add(guide)

    return render(request, 'submitted.html', context={'result': 'The excursion is updated!'})
    # else: return render(request, 'submitted.html', context={'result': 'Mistakes were made in filling out the form. Please correct the errors and resend again.'})


def send_message(request, id_excursion, chat_id):
    form = MessageForm(data=request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.chat_id = chat_id
        message.author_id = request.user.id
        message.save()

    return HttpResponseRedirect('/../jinrex/schedule/get_excursion/'+id_excursion)
