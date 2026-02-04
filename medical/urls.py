from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

app_name='medical'

router = DefaultRouter()
router.register(r'doctor', views.DoctorAPI, basename='doctor')
router.register(r'hos',views.HospitalAPI,basename='hos')
router.register(r'slot',views.slotsAPI,basename='slot')

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('hospital/',views.creation,name='hospital'),
    path('doc/',views.doctorregistration,name='doc'),
    path('patient/',views.patientview,name='patient'),
    path('slots/',views.slots,name='slots'),
    path('patientlist/',views.patientlist.as_view(),name='patientlist'),
    path('docearnings/',views.doctorearnings.as_view(),name='docearnings'),
]


urlpatterns+=router.urls