from django import forms
from django.forms import ModelForm
from .models import Excursion, Area, Facility, Organizator, Incharge, Guide

class ExcursionForm(ModelForm):
	date_excursion = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),input_formats=('%Y-%m-%d',))
	areas = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,queryset = Area.objects.all())
	class Meta:
		model = Excursion
		fields = ['id_excursion','facility', 'areas', 'organizator', 'guide', 'incharge',
		'occasion_excursion','date_excursion','time_period_excursion',
		'language_excursion','auditory_excursion','participants_excursion',
		'age_excursion']

		labels = {
			"facility": "Select facility",
			"areas": "Select areas",
			"guide": "Select desired guide",
			"participants_excursion": "Enter the number of participants",
			"age_excursion": "Enter the age of the participants",
        }