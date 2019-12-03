from django.contrib import admin
from .models import Excursion, Area, Facility, Incharge, Guide, Chat, Message, Phone

admin.site.register(Chat)
admin.site.register(Message)

admin.site.register(Excursion)
admin.site.register(Area)
admin.site.register(Facility)
admin.site.register(Incharge)
admin.site.register(Guide)
admin.site.register(Phone)