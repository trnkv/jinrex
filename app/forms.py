from django import forms
from django.forms import ModelForm
from .models import Excursion, Area, Facility, Organizator, Incharge, Guide

#class BlankForm(forms.Form):
#	"""Form for sending an application for an excursion."""
#	#facility = forms.ModelChoiceField(queryset=Facility, empty_label='Select facility')
#	#areas = forms.ChoiceField()
#	occasion = forms.CharField(label='Occasion', max_length=100)
#	date = forms.DateField()
#	time = forms.CharField(label='Time', max_length=100)

class ExcursionForm(ModelForm):
	date_excursion = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),input_formats=('%Y-%m-%d',))
	id_area = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple,queryset = Area.objects.all())
	class Meta:
		model = Excursion
		fields = ['id_excursion','id_facility', 'id_area', 'name_organizator', 'id_guide',
		'occasion_excursion','date_excursion','time_period_excursion',
		'language_excursion','auditory_excursion','participants_excursion',
		'age_excursion']

		labels = {
			"id_facility": "Select facility",
			"id_area": "Select areas",
			"id_guide": "Select desired guide",
			"participants_excursion": "Enter the number of participants",
			"age_excursion": "Enter the age of the participants",
        }