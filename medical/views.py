from django.shortcuts import render
from .serializers import Patientserializer,Doctorserializer,Hospitalserializer,Timingsserializer,registrationserializer,specilizationserilizer,loginserializer
from .models import Doctor,specialization,Hospital,patient,Timings,income
from .forms import Doctorform,patientform,specializationform,Timingsform,Hospitalform
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseForbidden
from django.shortcuts import render,get_object_or_404
from rest_framework import status,mixins,generics,viewsets
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
from django.db.models import Sum

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
@login_required                 
def creation(request):
    if not Hospital.objects.filter(user=request.user).exists():
        return HttpResponseForbidden("Hospital owners only")
    
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

class HospitalAPI(viewsets.ModelViewSet):
    serializer_class=Hospitalserializer
    http_method_names=['patch','get','delete']
    def get_queryset(self):
        return Hospital.objects.filter(user=self.request.user)
    
def doctorregistration(request):
    form=Doctorform()
    if request.method=="POST":
        form=Doctorform(request.POST)
        if form.is_valid():
            data=form.cleaned_data.copy()
            data['specializations']=[s.id for s in data['specializations']]
            data['hospitals']=[s.id for s in data['hospitals']]
            data['user']=request.user.id 
            
            serializer=Doctorserializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()       
            return HttpResponseRedirect(reverse('medical:home'))
            
    return render(request,'doctor.html',{'form':form})

from django.db import transaction

def patientview(request):
    form=patientform()
    if request.method=="POST":
        form=patientform(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form_obj = form.save(commit=False)
                form_obj.user = request.user
                form_obj.save()

                booking = form_obj.appointment   
                hos = form_obj.hospital
                doc = booking.user               

                docfee = doc.charge

                doctorfee = int(docfee * 0.6)
                hospitalfee = int(docfee * 0.4)

                income.objects.create(
                    appointment=form_obj,
                    docincome=doctorfee,
                    hospitalincome=hospitalfee
                )
            
    return render(request,'patient.html',{'form':form})  

class doctorearnings(ListView):
    model=income
    template_name='docearnings.html'
    context_object_name='earnings'
    def get_queryset(self):
        doctor=Doctor.objects.get(user=self.request.user)
        return income.objects.filter(
    appointment__appointment__user=doctor
).values(
    'appointment__hospital__id',
    'appointment__hospital__name'
).annotate(
    total_income=Sum('docincome')
)
    
    
class DoctorAPI(viewsets.ModelViewSet):
    serializer_class=Doctorserializer
    http_method_names=['get','delete','patch']
    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)


class patientlist(ListView):
    model=patient
    template_name='patientlist.html'
    context_object_name='pat'
    
def slots(request):
    form=Timingsform 
    
    if request.method=="POST":
        form=Timingsform(request.POST)
        if form.is_valid():
            data=form.cleaned_data.copy()
            data['user']=request.user.id 
            data['hospital']=data['hospital'].id 
            serializer=Timingsserializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
    
    return render(request,'slots.html',{'form':form})    

class slotsAPI(viewsets.ModelViewSet):
    serializer_class=Timingsserializer
    http_method_names=['get','delete','patch']
    def get_queryset(self):
        doctor=Doctor.objects.get(user=self.request.user)
        return Timings.objects.filter(user=doctor)