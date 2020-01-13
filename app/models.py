from django.db import models
import uuid # Required for unique instances
from django.contrib.auth.models import  User, Group, Permission
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse #Used to generate URLs by reversing the URL patterns


# Create your models here.
class Phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,17}$', message="Phone number must be entered in the format: '+71234567890'. Up to 17 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,  unique=True) # validators should be a list

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name() + " (@" + self.user.get_username() + ') : ' + self.phone_number

class Facility(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.AutoField(primary_key=True, help_text="Unique ID for this facility")
    name = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular facility.
        """
        return reverse('facility-detail', args=[str(self.id)])


class Area(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    id = models.AutoField(primary_key=True, help_text="Unique ID for this particular area")
    facility = models.ManyToManyField(Facility)
    name = models.CharField(max_length=200)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Foreign Key used because book can only have one author, but authors can have multiple books

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular area.
        """
        return reverse('area-detail', args=[str(self.id)])


class Incharge(models.Model):
    """
    Model representing a person incharge of the excursion.
    """
    facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name() + ' (@' + self.user.get_username() + ')'


class Guide(models.Model):
    facility = models.ManyToManyField(Facility)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name() + ' (@' + self.user.get_username() + ')'


class Excursion(models.Model):
    """
    Model representing an excursion.
    """
    id = models.AutoField(verbose_name='id_excursion', serialize=False, auto_created=True, primary_key=True)
    facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    areas = models.ManyToManyField(Area)

    organizator = models.ForeignKey(User, related_name='user_organizator', default="", on_delete=models.DO_NOTHING)
    guide = models.ForeignKey(Guide, related_name='user_guide', default="", on_delete=models.DO_NOTHING)
    incharge = models.ForeignKey(Incharge, related_name='user_incharge', default="", on_delete=models.DO_NOTHING)

    occasion = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=timezone.now)
    stop_time = models.TimeField(default=timezone.now)
    language = models.CharField(max_length=200)
    auditory = models.CharField(max_length=200)
    participants = models.IntegerField()

    confirmed_guide = models.BooleanField(default=False)
    confirmed_incharge = models.BooleanField(default=False)


    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s, %s' % (self.facility, self.date)

# Модели для реализации чата
class Chat(models.Model):
    excursion = models.OneToOneField(Excursion, on_delete=models.DO_NOTHING)
    members = models.ManyToManyField(User, verbose_name=_("Member"))

    def get_absolute_url(self):
        return reverse('messages', (), {'chat_id': self.pk })

    def __str__(self):
        return str(self.excursion)


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.DO_NOTHING)
    message = models.TextField(_("Message"))
    pub_date = models.DateTimeField(_('Date'), default=timezone.now)
    is_readed = models.BooleanField(_('Readed'), default=False)

    class Meta:
        ordering=['pub_date']

    def __str__(self):
        return self.pub_date.strftime('%d/%m/%Y, %H:%M:%S') + ", \"" + str(self.chat) + "\": " + str(self.author)
