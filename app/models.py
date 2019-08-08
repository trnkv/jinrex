from django.db import models
import uuid # Required for unique instances

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
    name_organizator = models.CharField(max_length=100)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.name_organizator)

    
    def get_absolute_url(self):
        """
        Returns the url to access a particular organizator instance.
        """
        return reverse('organizator-detail', args=[str(self.id_organizator)])


class Incharge(models.Model):
    """
    Model representing a person in charge of the excursion.
    """
    id_incharge = models.AutoField(primary_key=True)
    id_facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    firstName_incharge = models.CharField(max_length=100)
    lastName_incharge = models.CharField(max_length=100)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.firstName_incharge, self.lastName_incharge)

    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('organizator-detail', args=[str(self.id_incharge)])


class Guide(models.Model):
    """
    Model representing a person in charge of the excursion.
    """
    id_guide = models.AutoField(primary_key=True)
    firstName_guide = models.CharField(max_length=100)
    lastName_guide = models.CharField(max_length=100)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.firstName_guide, self.lastName_guide)

    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('guide-detail', args=[str(self.id_guide)])


class Excursion(models.Model):
    """
    Model representing an excursion.
    """
    id_excursion = models.AutoField(verbose_name='id_excursion', serialize=False, auto_created=True, primary_key=True, help_text="Unique ID for this particular excursion")
    id_facility = models.ForeignKey('Facility', on_delete=models.DO_NOTHING)
    id_area = models.ManyToManyField(Area, help_text="Select a desired areas for this excursion")
    name_organizator = models.CharField(max_length=200)
    id_guide = models.ForeignKey('Guide', on_delete=models.DO_NOTHING)
    occasion_excursion = models.CharField(max_length=200, help_text="Enter an excursion occasion (e.g. JEMS 12 etc.)")
    date_excursion = models.DateField(null=True,help_text="Enter an excursion date")
    time_period_excursion = models.CharField(max_length=200, help_text="Enter an excursion time period")
    language_excursion = models.CharField(max_length=200, help_text="Enter an excursion language")
    auditory_excursion = models.CharField(max_length=200, help_text="Enter an excursion auditory")
    participants_excursion = models.IntegerField(help_text="Enter count of an excursion participants")
    age_excursion = models.CharField(max_length=6, help_text="Enter an age of excursion participants")


    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s, %s' % (self.occasion_excursion, self.date_excursion)

