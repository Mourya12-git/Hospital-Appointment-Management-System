from django.urls import path,include
from . import views

app_name='medical'

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.loginuser,name='login'),
    path('logout/',views.logoutuser,name='logout'),
    path('hospital/',views.creation,name='hospital'),
]