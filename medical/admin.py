from django.contrib import admin
from .models import Hospital,specialization,patient,Timings,Doctor
# Register your models here.

admin.site.register(specialization)
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Timings)
admin.site.register(patient)
