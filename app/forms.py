from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission
from .models import Excursion, Area, Facility, Incharge, Message


class MessageForm(ModelForm):
	class Meta:
		model = Message
		widgets = {
			'message': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
		}
		fields = ['message']
		labels = {'message': ""}


class SendExcursionForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(SendExcursionForm, self).__init__(*args, **kwargs)

		guides = Group.objects.get(name='Guide').user_set.all().values()
		choices_guide = [('0', '---------')]
		choices_guide += ([(s['id'], '%s %s (@%s)' % (s['first_name'], s['last_name'], s['username'])) for s in guides])
		self.fields['guide'].choices = choices_guide

	# incharges = Incharge.objects.filter(id_facility=self.fields['facility'].queryset[0]).values()
	# incharges = Group.objects.get(name='Incharge').user_set.all().values()

	# choices_incharge = [('0', '---------')]
	# choices_incharge += ([(s['id'] ,'%s %s (@%s)' % (s['first_name'], s['last_name'], s['username'])) for s in incharges])
	# self.fields['incharge'].choices = choices_incharge
	# i = Incharge.objects.filter(id_facility=self.fields['facility'].queryset[0]).values('user_id')[0]['user_id']

	date_excursion = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))
	areas = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Area.objects.all())

	class Meta():
		model = Excursion
		fields = ['id_excursion', 'facility', 'areas', 'guide',
				  'occasion_excursion', 'date_excursion', 'time_period_excursion',
				  'language_excursion', 'auditory_excursion', 'participants_excursion',
				  'age_excursion']

		labels = {
			"facility": "Select facility",
			"areas": "Select areas",
			"guide": "Select desired guide",
			"participants_excursion": "Enter the number of participants",
			"age_excursion": "Enter the age of the participants", }


class ViewExcursionForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ViewExcursionForm, self).__init__(*args, **kwargs)
		guides = Group.objects.get(name='Guide').user_set.all().values()
		choices_guide = []
		choices_guide += ([(s['id'], '%s %s (@%s)' % (s['first_name'], s['last_name'], s['username'])) for s in guides])
		self.fields['guide'].choices = choices_guide

		incharges = Incharge.objects.filter(id_facility=self.fields['facility'].queryset[0]).values()
		incharges = Group.objects.get(name='Incharge').user_set.all().values()

		choices_incharge = [('0', '---------')]
		choices_incharge += ([(s['id'] ,'%s %s (@%s)' % (s['first_name'], s['last_name'], s['username'])) for s in incharges])
		self.fields['incharge'].choices = choices_incharge
		# i = Incharge.objects.filter(id_facility=self.fields['facility'].queryset[0]).values('user_id')[0]['user_id']

	date_excursion = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))
	areas = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Area.objects.all())

	class Meta():
		model = Excursion
		fields = ['id_excursion', 'facility', 'areas', 'organizator', 'incharge', 'guide',
				  'occasion_excursion', 'date_excursion', 'time_period_excursion',
				  'language_excursion', 'auditory_excursion', 'participants_excursion',
				  'age_excursion']
