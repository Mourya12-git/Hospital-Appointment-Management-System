from .models import Hospital,specialization,patient,Timings,Doctor
from rest_framework import serializers
from django.contrib.auth.models import User

class registrationserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta():
        model=User
        fields=('username','password',)
        
    def create(self, validated_data):
        user=User.objects.create_user(                               #
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class Hospitalserializer(serializers.ModelSerializer):
    class Meta():                                                                               #
        model=Hospital
        fields=('user','name','location','specilaizations','charge',)
        
class specilizationserilizer(serializers.ModelSerializer):
    class Meta():
        model=specialization
        fields=('sspecialities',)

class Doctorserializer(serializers.ModelSerializer):
    class meta():                                                                                               #
        model=Doctor
        fields=('name','specializations','hospitals','charge',)

class Timingsserializer(serializers.ModelSerializer):
    class Meta():                                                                                               #
        model=Timings
        fields=('name','hospital','starttime','endtime',)
        
class Patientserializer(serializers.ModelSerializer):
    class Meta():
        model=patient
        fields=('name','age','hospital','appointment',)                                                          #
        
class loginserializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

