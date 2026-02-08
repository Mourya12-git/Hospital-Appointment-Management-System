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
        exclude = ['user']
        
class patientform(forms.ModelForm):
    class Meta():
        model=patient
        exclude = ['user']
        fields=('age','hospital','appointment')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['appointment'].queryset = Timings.objects.filter(
                booked=False
            )

class Timingsform(forms.ModelForm):
    class Meta():
        model=Timings
        exclude = ['user','booked']
        
class specializationform(forms.ModelForm):
    class Meta():
        model=specialization
        fields=('specialities',)