from django.contrib import admin

from .models import Excursion, Area, Facility, Organizator, Incharge, Guide

admin.site.register(Excursion)
admin.site.register(Area)
admin.site.register(Facility)
admin.site.register(Organizator)
admin.site.register(Incharge)
admin.site.register(Guide)