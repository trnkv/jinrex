from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Excursion, Area, Facility, Organizator, Incharge, Guide

class ExcursionDelete(DeleteView):
    model = Excursion
    success_url = reverse_lazy('schedule')

    #def get_queryset(self):
         #queryset = super().get_queryset()
         #return queryset.filter(recipient = self.request.user)

    def delete(self,*args,**kwargs):
    	#messages.success(self.request,'Excursion Deleted')
    	return super().delete(*args,**kwargs)