from django import forms
from .models import Hospital,Doctor,patient,Timings,specialization
from django.contrib.auth.models import User


class Hospitalform(forms.ModelForm):
    class Meta():
        model=Hospital
        exclude = ['user']
        
class Doctorform(forms.ModelForm):
    class Meta():
        model=Doctor
        fields=('specializations','charge','hospitals')
        
class patientform(forms.ModelForm):
    class Meta():
        model=patient
        fields=('age','hospital','appointment')

class Timingsform(forms.ModelForm):
    class Meta():
        model=Timings
        fields=('hospital','starttime','endtime')
        
class specializationform(forms.ModelForm):
    class Meta():
        model=specialization
        fields=('specialities',)