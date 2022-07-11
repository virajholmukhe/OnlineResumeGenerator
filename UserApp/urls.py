
from django.contrib import admin
from django.urls import path
from UserApp import views

urlpatterns = [
    path('',views.home),

    path('signup',views.signup),
    path('login',views.login),
    path('logout',views.logout),

    path('personal_info',views.personal_information),
    path('delete_resume/<pid>',views.delete_personal_info),
    path('dashboard/<pid>',views.dashboard, name='dashboard'),
    #path('fields',views.fields),
    path('educational_Details/<Pers>',views.educational_Details),
    path('Certification/<Pers>',views.Certification),
    path('Technical_Skills/<Pers>',views.Technical_Skills),
    path('Academic_Project/<Pers>',views.Academic_Project),
    path('resume',views.resume),

    path('pdf/<pid>', views.showPdf),
    path('contact_us',views.contactUs),
    path('save/<pid>',views.saveResume),
    path('my_resumes', views.my_Resumes),
    
]
