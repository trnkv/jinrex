"""
Generates random excursion and its data.
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jinrex.settings")
import django
django.setup()
import sys
sys.path.append('app/')
from app.models import Facility, Area, Organizator, Guide, Incharge, Excursion, Chat
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import random
import sys
import datetime
import string
import csv


def get_random_string(length):
    symbols = string.ascii_letters
    s = ''
    for _ in range(length):
        s += random.choice(symbols)
    return s


def generate_facility():
    facility_names = ('LIT', 'LHEP', 'LRB', 'FLNP',
                      'DLNP', 'BLTP', 'FLNR', 'UC')
    new_facility, is_created = Facility.objects.get_or_create(
        name=random.choice(facility_names)
    )
    if is_created:
        new_facility.save()
    return new_facility


def generate_area(facilities_list):
    area_names = ('Photos', 'Museum', 'Lectures', 'MICC', 'MICC CR')
    new_area, is_created = Area.objects.get_or_create(
        name=random.choice(area_names),
    )
    if is_created:
        new_area.facility.set(facilities_list)
        new_area.save()
    else:
        for f in facilities_list:
            new_area.facility.add(f)
    return new_area


def generate_user():
    first_names = ('Никанор', 'Илья', 'Лев', 'Альбина', 'Аскольд', 'Ираида',
                   'Евгения', 'Ярослав', 'Самуил', 'Анна', 'Ярослава', 'Степан')
    last_names = ('Johnson', 'Smith', 'Williams', 'Jones', 'Miller', 'Taylor')

    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'yu', 'я': 'ya', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'yo',
              'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
              'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'h',
              'Ц': 'c', 'Ч': 'ch', 'Ш': 'sh', 'Щ': 'sch', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e',
              'Ю': 'yu', 'Я': 'ya'}

    user_f_name = random.choice(first_names)
    user_l_name = random.choice(last_names)

    f_name_translit = user_f_name

    for key in slovar:
        f_name_translit = f_name_translit.replace(key, slovar[key])

    username = f_name_translit+"_"+user_l_name

    # create user
    new_user, is_created = User.objects.get_or_create(
        username=username,
        first_name=user_f_name,
        last_name=user_l_name,
    )
    if is_created:
        new_user.set_password('1')
        new_user.save()
    return new_user


def generate_user_by_username(username):
    # create user
    new_user, is_created = User.objects.get_or_create(
        username=username,
        first_name=username,
        last_name=username,
    )
    if is_created:
        new_user.set_password('1')
        new_user.save()
    return new_user


def add_guide(facility_name):
    try:
        existing_guide = Guide.objects.get(
            facility=Facility.objects.get(name=facility_name))
        return existing_guide
    except ObjectDoesNotExist:
        user = generate_user()
        # user.groups.add(Group.objects.get(name='Guide'))
        new_guide, is_created = Guide.objects.get_or_create(
            user=user,
        )
        if is_created:
            new_guide.facility.set([Facility.objects.get(name=facility_name)])
            new_guide.save()
        return new_guide


def make_user_guide(facility_name, user):
    new_guide, is_created = Guide.objects.get_or_create(
        user=user,
    )
    if is_created:
        new_guide.facility.set([Facility.objects.get(name=facility_name)])
        new_guide.save()
    return new_guide


def add_incharge(facility_name):
    try:
        existing_incharge = Incharge.objects.get(
            facility=Facility.objects.get(name=facility_name))
        return existing_incharge
    except ObjectDoesNotExist:
        user = generate_user()
        # user.groups.add(Group.objects.get(name='Incharge'))
        new_incharge, is_created = Incharge.objects.get_or_create(
            user=user,
            facility=Facility.objects.get(name=facility_name)
        )
        if is_created:
            new_incharge.save()
        return new_incharge


def make_user_incharge(facility_name, user):
    new_incharge, is_created = Incharge.objects.get_or_create(
        user=user,
        facility = Facility.objects.get(name=facility_name)
    )
    return new_incharge


def add_organizator(user):
    new_org, is_created = Organizator.objects.get_or_create(user=user)
    if is_created:
        new_org.save()
    # user.groups.add(Group.objects.get(name='Organizator'))
    return new_org


def generate_excursion(facility, areas, organizator, guide, incharge):
    new_excursion, is_created = Excursion.objects.get_or_create(
        facility=facility,
        organizator=organizator,
        guide=guide,
        incharge=incharge,
        event=get_random_string(5),
        date=datetime.date.today(),
        start_time=datetime.datetime.now().time(),
        stop_time=datetime.datetime.now().time(),
        language='English',
        target_audience='Students',
        participants=12
    )
    if is_created:
        new_excursion.areas.set([areas])
        new_excursion.save()
        new_chat = Chat.objects.create(
            excursion=new_excursion
        )
        new_chat.members.add(new_excursion.organizator.user)
        new_chat.members.add(new_excursion.guide.user)
        new_chat.members.add(new_excursion.incharge.user)
    else:
        new_excursion.areas.add(a for a in areas)
    return new_excursion


def main():
    # facility = generate_facility()
    # area = generate_area([facility])
    # guide = add_guide(facility.name)
    # incharge = add_incharge(facility.name)
    # organizator = add_organizator(generate_user())

    with open('test_users/incharges.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # the below statement will skip the first row
        next(csv_reader)
        for row in csv_reader:
            new_user = generate_user_by_username(row[0])
            make_user_incharge(row[2], new_user)
            print('Created Incharge = %s in Facility = %s' % (row[0], row[2]))

    with open('test_users/guides.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # the below statement will skip the first row
        next(csv_reader)
        for row in csv_reader:
            new_user = generate_user_by_username(row[0])
            make_user_guide(row[2], new_user)
            print('Created Guide = %s in Facility = %s' % (row[0], row[2]))

    # excursion = generate_excursion(facility, area, organizator, guide, incharge)
    # print('Generated! The excursion info: \n')
    # print('Facility: ', excursion.facility.name, "\n")
    # print('Areas: ', excursion.areas.all(), "\n")
    # print('Organizator: ', excursion.organizator.user.get_full_name(), "\n")
    # print('Guide: ', excursion.guide.user.get_full_name(), "\n")
    # print('Icharge: ', excursion.incharge.user.get_full_name(), "\n")
    # print('Event: ', excursion.event, "\n")
    # print('Date: ', excursion.date, "\n")
    # print('Start Time: ', excursion.start_time, "\n")
    # print('Stop Time: ', excursion.stop_time, "\n")
    # print('Language: ', excursion.language, "\n")
    # print('Target Audience: ', excursion.target_audience, "\n")
    # print('Participants: ', excursion.participants)
    # print('------------------------------------')


if __name__ == "__main__":
    main()
