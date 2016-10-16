from django.contrib import admin

from .models import *

admin.site.register(Mandal)
admin.site.register(Employee)
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(Device)
admin.site.register(Incident)
admin.site.register(IncidentActions)
admin.site.register(IncidentWork)

