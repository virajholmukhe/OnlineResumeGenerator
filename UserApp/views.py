from django.shortcuts import redirect, render,HttpResponse
from UserApp.models import User_Info, published_resumes,personal_info,educational_details,certification,technical_skills,academic_project,ContactMe
from django.contrib import messages
from .process import html_to_pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files import File
from io import BytesIO

# Create your views here.
def home(request):
    try:
        request.session["uname"]
        all_pdfs = published_resumes.objects.all()
        return render(request, 'home.html',{"all_pdfs":all_pdfs})
    except:
        return render(request,"home.html")

def signup(request):
    if(request.method == "GET"):
        request.session.clear()
        return render(request,"signup.html",{})
    else:
        uname=request.POST['Username']
        pwd=request.POST['pswd']
        if User_Info.objects.filter(username=uname).exists():
            error_msg = "username: "+uname+" is already exist"
            messages.error(request, error_msg)
            return render(request,"signup.html",{})
        else:
            u1=User_Info()
            u1.username=uname
            u1.password=pwd
            u1.save()
            return redirect(login)

def login(request):
    if(request.method == "GET"):
        request.session.clear()
        return render(request,"login.html",{})
    else:
        uname=request.POST["Username"]
        pwd=request.POST["pswd"]
        try:
            u1=User_Info.objects.get(username=uname,password=pwd)
            #create a session
            request.session["uname"]=uname
            #return HttpResponse("successfully login")
        except:
            messages.error(request, 'invalid username or password')
            return render(request,"login.html")
            #return HttpResponse("login fail")
        return redirect(home)

def logout(request):
    request.session.clear()
    return redirect(home)

def dashboard(request,pid):
    try:
        uname = request.session["uname"]
        personal_info.objects.get(user=uname,id=pid)
        pers_info = personal_info.objects.get(user=uname,id=pid)
        edu_info = educational_details.objects.filter(perIn_id=pers_info.id)
        cert_info = certification.objects.filter(perIn_id=pers_info.id)
        tech_sk_info = technical_skills.objects.filter(perIn_id=pers_info.id)
        aca_pr_info = academic_project.objects.filter(perIn_id=pers_info.id)
        if(request.method=='POST'):
            if(request.POST['action']=="delete_technical_skill"):
                tech_sk_info = technical_skills.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            elif(request.POST['action']=="delete_educational_detail"):
                edu_info = educational_details.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            elif(request.POST['action']=="delete_certification_detail"):
                cert_info = certification.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            elif(request.POST['action']=="delete_academic_project_detail"):
                aca_pr_info = academic_project.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            return redirect('dashboard',pid = pers_info.id)
        else:
            return render(request, "dashboard.html",{"pi":pers_info,"ei":edu_info,"ci":cert_info,"ti":tech_sk_info,"ai":aca_pr_info})
    except:
        return redirect(personal_information)

def my_Resumes(request):
    uname = request.session["uname"]
    pers_info = personal_info.objects.filter(user=uname)
    return render(request, 'my_resumes.html',{"pi":pers_info})

def personal_information(request):
    if(request.method == "GET"):
        if("uname" in request.session):
            return render(request,"personal_info.html",{})
        else:
            return redirect(login)
    else:
        p1=personal_info()
        p1.fullname=request.POST['fullname']
        p1.phone_number=request.POST['phone_number']
        p1.Gender=request.POST['Gender']
        p1.dob=request.POST['dob']
        p1.emailid=request.POST['emailid']
        p1.Address=request.POST['Address']
        p1.hobbies=request.POST['hobbies']
        p1.languages_known=request.POST['languages_known']
        p1.linkedin=request.POST['linkedin']
        p1.github=request.POST['github']
        p1.objective=request.POST['objective']
        uname = request.session["uname"]
        user = User_Info.objects.get(username=uname)
        p1.user = user
        p1.save()
        pid = p1.id
        #return redirect(fields)
        return redirect('dashboard',pid)

def delete_personal_info(request,pid):
    if("uname" in request.session):
        pi = personal_info.objects.get(user=request.session['uname'],id=pid)
        pi.delete()
        return redirect(my_Resumes)
    else:
        return redirect(login)

def educational_Details(request,Pers):
    if (request.method =="GET"):
        return render(request,"educational_details.html",{"Pers":Pers})  
    else:
        e1=educational_details()
        e1.nameOfExamination=request.POST['nameOfExamination']
        e1.institute=request.POST['institute']
        e1.university=request.POST['university']
        e1.percentage=request.POST['percentage']
        e1.yearOfcompletion=request.POST['yearOfcompletion']
        e1.perIn_id=personal_info.objects.get(id=Pers)
        e1.save()
        return redirect('dashboard',Pers)
    
def Certification(request,Pers):
    if (request.method =="GET"):
        return render(request,"Certification.html",{"Pers":Pers})  
    else:
        c1=certification()
        c1.certification=request.POST['certification']
        c1.perIn_id=personal_info.objects.get(id=Pers)
        c1.save()
        return redirect('dashboard',Pers)  
        
def Technical_Skills(request,Pers):
    if (request.method =="GET"):
        return render(request,"Technical_Skills.html",{"Pers":Pers})
    else:
        t1=technical_skills()
        t1.skills=request.POST['skills']
        t1.perIn_id=personal_info.objects.get(id=Pers)
        t1.save()
        return redirect('dashboard',Pers)
        
def Academic_Project(request,Pers):
    if (request.method =="GET"):
        return render(request,"Academic_Project.html",{"Pers":Pers})
    else:
        a1=academic_project()
        a1.project_name=request.POST['project_name']
        a1.project_title=request.POST['project_title']
        a1.technologies_used=request.POST['technologies_used']
        a1.description=request.POST['description']
        a1.perIn_id=personal_info.objects.get(id=Pers)
        a1.save()
        return redirect('dashboard',Pers)
    
def resume(request):
    return render(request,"resume.html",{})

def contactUs(request):
    if(request.method == "GET"):
        return render(request,'contact_us.html',{})
    else:
        obj = ContactMe()
        obj.name = request.POST["name"]
        obj.email = request.POST["email"]
        obj.subject = request.POST["subject"]
        obj.message = request.POST["message"]
        obj.save()
        return redirect(home)
        
def showPdf(request,pid):
    uname = request.session["uname"]
    Pers=personal_info.objects.get(user=uname,id=pid)
    Ed_d=educational_details.objects.filter(perIn_id=Pers.id)
    certi=certification.objects.filter(perIn_id=Pers.id)
    Tec_Skill=technical_skills.objects.filter(perIn_id=Pers.id)
    acd_p=academic_project.objects.filter(perIn_id=Pers.id)
    open('UserApp/templates/temp.html', "w").write(render_to_string('Resume.html', {"Ed_d":Ed_d,"certi":certi,"Tec_Skill":Tec_Skill,"acd_p":acd_p,"Pers":Pers}))
    pdf = html_to_pdf('temp.html')
    #print(type(pdf))
    return HttpResponse(pdf, content_type='application/pdf')

def saveResume(request,pid):
    uname = request.session["uname"]
    Pers=personal_info.objects.get(user=uname,id=pid)
    Ed_d=educational_details.objects.filter(perIn_id=Pers.id)
    certi=certification.objects.filter(perIn_id=Pers.id)
    Tec_Skill=technical_skills.objects.filter(perIn_id=Pers.id)
    acd_p=academic_project.objects.filter(perIn_id=Pers.id)
    open('UserApp/templates/temp.html', "w").write(render_to_string('Resume.html', {"Ed_d":Ed_d,"certi":certi,"Tec_Skill":Tec_Skill,"acd_p":acd_p,"Pers":Pers}))
    myCV = published_resumes()
    pdf = html_to_pdf('temp.html')
    filename = f'{uname}-{Pers.id}.pdf'
    myCV.user = User_Info.objects.get(username=uname)
    myCV.person_info = personal_info.objects.get(user=uname,id=pid)
    myCV.resume.save(filename, File(BytesIO(pdf.content)))
    return redirect(my_Resumes)


