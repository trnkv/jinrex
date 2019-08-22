from django.db import models
import uuid # Required for unique instances
from django.contrib.auth.models import User

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


from django.urls import reverse #Used to generate URLs by reversing the URL patterns


class Organizator(models.Model):
    """
    Model representing an excursion organizator.
    """
    id_organizator = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name()


class Incharge(models.Model):
    """
    Model representing a person in charge of the excursion.
    """
    id_incharge = models.AutoField(primary_key=True)
    id_facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.get_full_name()


class Guide(models.Model):
    """
    Model representing a person in charge of the excursion.
    """
    id_guide = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")

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
    facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING, help_text="Select desired facility")
    areas = models.ManyToManyField(Area, help_text="Select a desired areas for this excursion")

    organizator = models.ForeignKey(Organizator, related_name='user_organizator', default="", on_delete=models.DO_NOTHING, help_text="Enter the name of the excursion organizator")
    guide = models.ForeignKey(Guide, related_name='user_guide', default="", on_delete=models.DO_NOTHING, help_text="Select desired guide for this excursion")
    incharge = models.ForeignKey(Incharge, related_name='user_incharge', default="", on_delete=models.DO_NOTHING, help_text="Responsible for the excursion")
    
    occasion_excursion = models.CharField(max_length=200, help_text="Enter occasion of excursion  (e.g. JEMS 12 etc.)")
    date_excursion = models.DateField(help_text="Enter date of excursion")
    time_period_excursion = models.CharField(max_length=200, help_text="Enter time period of excursion")
    language_excursion = models.CharField(max_length=200, help_text="Enter language of excursion")
    auditory_excursion = models.CharField(max_length=200, help_text="Enter auditory of excursion ")
    participants_excursion = models.IntegerField(help_text="Enter count of excursion participants")
    age_excursion = models.CharField(max_length=6, help_text="Enter age of excursion participants")

    confirmed = models.BooleanField(default=False)


    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s, %s' % (self.facility, self.date_excursion)

