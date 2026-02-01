from django.db import models
from django.contrib.auth.models import User
# Create your models here.
  
class specialization(models.Model):
    specialities=models.CharField(max_length=100)
    
    def __str__(self):
        return self.specialities

class Hospital(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    specilaizations=models.ManyToManyField(specialization)
    charge=models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    specializations=models.ManyToManyField(specialization)
    hospitals=models.ManyToManyField(Hospital)
    charge=models.PositiveIntegerField()

class Timings(models.Model):
    user=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    starttime=models.DateTimeField()
    endtime=models.TimeField()
    
class patient(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    hospital=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    appointment=models.ForeignKey(Timings,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    