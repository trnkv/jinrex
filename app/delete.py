from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Excursion, Area, Facility, Organizator, Incharge, Guide

class ExcursionDelete(DeleteView):
    model = Excursion
    success_url = reverse_lazy('schedule')