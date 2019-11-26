from django.contrib import admin
from .models import Excursion, Area, Facility, Incharge, Chat, Message

admin.site.register(Chat)
admin.site.register(Message)

admin.site.register(Excursion)
admin.site.register(Area)
admin.site.register(Facility)
admin.site.register(Incharge)