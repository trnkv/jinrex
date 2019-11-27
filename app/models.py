from django.db import models
import uuid # Required for unique instances
from django.contrib.auth.models import User, Group, Permission
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
class Facility(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id_facility = models.AutoField(primary_key=True, help_text="Unique ID for this facility")
    name_facility = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name_facility

    def get_absolute_url(self):
        """
        Returns the url to access a particular facility.
        """
        return reverse('facility-detail', args=[str(self.id_facility)])


class Area(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    id_area = models.AutoField(primary_key=True, help_text="Unique ID for this particular area")
    id_facility = models.ManyToManyField(Facility)
    name_area = models.CharField(max_length=200)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Foreign Key used because book can only have one author, but authors can have multiple books
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name_area
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular area.
        """
        return reverse('area-detail', args=[str(self.id_area)])


class Incharge(models.Model):
    """
    Model representing a person incharge of the excursion.
    """
    id_facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name()


class Excursion(models.Model):
    """
    Model representing an excursion.
    """
    id_excursion = models.AutoField(verbose_name='id_excursion', serialize=False, auto_created=True, primary_key=True, help_text="Unique ID for this particular excursion")
    facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    areas = models.ManyToManyField(Area)

    organizator = models.ForeignKey(User, related_name='user_organizator', default="", on_delete=models.DO_NOTHING, help_text="Organizator of this excursion")
    guide = models.ForeignKey(User, related_name='user_guide', default="", on_delete=models.DO_NOTHING)
    incharge = models.ForeignKey(User, related_name='user_incharge', default="", on_delete=models.DO_NOTHING, help_text="Responsible for the excursion")
    
    occasion_excursion = models.CharField(max_length=200)
    date_excursion = models.DateField(help_text="Enter date of excursion")
    time_period_excursion = models.CharField(max_length=200)
    language_excursion = models.CharField(max_length=200)
    auditory_excursion = models.CharField(max_length=200)
    participants_excursion = models.IntegerField()
    age_excursion = models.CharField(max_length=6)

    confirmed_guide = models.BooleanField(default=False)
    confirmed_incharge = models.BooleanField(default=False)


    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s, %s' % (self.facility, self.date_excursion)

# Модели для реализации чата
class Chat(models.Model):
    excursion = models.OneToOneField(Excursion, on_delete=models.DO_NOTHING)
    members = models.ManyToManyField(User, verbose_name=_("Member"))
    
    def get_absolute_url(self):
        return reverse('messages', (), {'chat_id': self.pk })
 
 
class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Chat"), on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.DO_NOTHING)
    message = models.TextField(_("Message"))
    pub_date = models.DateTimeField(_('Date'), default=timezone.now)
    is_readed = models.BooleanField(_('Readed'), default=False)
 
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message