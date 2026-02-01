from django.shortcuts import render
from .serializers import Patientserializer,Doctorserializer,Hospitalserializer,Timingsserializer,registrationserializer,specilizationserilizer,loginserializer
from .models import Doctor,specialization,Hospital,patient,Timings
from .forms import Doctorform,patientform,specializationform,Timingsform,Hospitalform
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

def home(request):
    return HttpResponse('HELLO')

def register(request):
    reg=registrationserializer()
    if request.method=="POST":
        reg=registrationserializer(data=request.POST)
        if reg.is_valid():
            reg.save()
            return HttpResponseRedirect(reverse('medical:login'))
        else:
            print(reg.errors)
    return render(request,'register.html',{'users':reg})

def loginuser(request):
    register=loginserializer()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('medical:hospital'))
        else:
            return HttpResponseRedirect(reverse('medical:register'))
        
    return render(request,'login.html')

@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('medical:register'))
            
        
def creation(request):
    form = Hospitalform()

    if request.method == "POST":
        form = Hospitalform(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            data['specilaizations'] = [s.id for s in data['specilaizations']]
            data['user'] = request.user.id

            serializer = Hospitalserializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return HttpResponseRedirect(reverse('medical:home'))

    return render(request,'admin.html',{'form':form})
    
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