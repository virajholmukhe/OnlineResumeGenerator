
from django.contrib import admin
from django.urls import path
from UserApp import views

urlpatterns = [
    path('',views.home),
    path('signup',views.signup),
    path('login',views.login),
    path('logout',views.logout),
    path('personal_info',views.personal_information),
    path('dashboard',views.dashboard),
    #path('fields',views.fields),
    path('educational_Details/<Pers>',views.educational_Details),
    path('Certification/<Pers>',views.Certification),
    path('Technical_Skills/<Pers>',views.Technical_Skills),
    path('Academic_Project/<Pers>',views.Academic_Project),
    path('resume',views.resume),

    path('pdf', views.generatePdf),
    path('contact_us',views.contactUs),
    
]
