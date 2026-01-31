from django.shortcuts import render
from .serializers import Patientserializer,Doctorserializer,Hospitalserializer,Timingsserializer,registrationserializer,specilizationserilizer,loginserializer
from .models import Doctor,specialization,Hospital,patient,Timings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import View,TemplateView,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse,reverse_lazy
from django.shortcuts import redirect
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework import filters

def register(request):
    reg=registrationserializer()
    if request.method=="POST":
        reg=registrationserializer(request.POST)
        reg.save()
    return render(request,'register.html',{'users':reg})

def loginuser(request):
    register=loginserializer()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        
        if user:
            if user.is_active():
                login(request,user)
                return HttpResponseRedirect(reverse('medical:home'))
        else:
            return HttpResponseRedirect(reverse('medical:register'))
        
    return render(request,'login.html')

@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('medical:home'))
            
        
def creation(request):
    serializer=Hospitalserializer()
    if request.method=="POST":
        serializer=Hospitalserializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            
    return render(request,'admin.html',{'serializer':serializer})
    
def doctorregistration(request):
    serializer=Doctorserializer()
    if request.method=="POST":
        serializer=Doctorserializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()           
    return render(request,'doctor.html',{'serializer':serializer})
    
    
def patientview(request):
    serializer=Patientserializer()
    if request.method=="POST":
        serializer=Patientserializer(data=request.POST)
        if serializer.is_valid():            
            serializer.save()
    return render(request,'patient.html',{'serializer':serializer})    
    
def slots(request):
    serializer=Timingsserializer()
    if request.method=="POST":
        serializer=Timingsserializer(data=request.POST)
    if serializer.is_valid():
        serializer.save()
    
    return render(request,'slots.html',{'serializer':serializer})    