from django.shortcuts import redirect, render,HttpResponse
from UserApp.models import User_Info,personal_info,educational_details,certification,technical_skills,academic_project,ContactMe
from django.contrib import messages

# Create your views here.
def home(request):
    try:
        request.session["uname"]
        try:
            personal_info.objects.get(user=request.session["uname"])
            shouldFill = True
            return render(request,"home.html",{"fill":shouldFill})
        except:
            shouldFill = False
            return render(request,"home.html",{"fill":shouldFill})
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

def dashboard(request):
    try:
        uname = request.session["uname"]
        personal_info.objects.get(user=uname)
        
        pers_info = personal_info.objects.get(user=uname)
        edu_info = educational_details.objects.filter(perIn_id=pers_info.id)
        cert_info = certification.objects.filter(perIn_id=pers_info.id)
        tech_sk_info = technical_skills.objects.filter(perIn_id=pers_info.id)
        aca_pr_info = academic_project.objects.filter(perIn_id=pers_info.id)

        if(request.method=='POST'):
            if(request.POST['action']=="delete_technical_skill"):
                tech_sk_info = technical_skills.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
                return redirect(dashboard)
            elif(request.POST['action']=="delete_educational_detail"):
                edu_info = educational_details.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            elif(request.POST['action']=="delete_certification_detail"):
                cert_info = certification.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            elif(request.POST['action']=="delete_academic_project_detail"):
                aca_pr_info = academic_project.objects.filter(perIn_id=pers_info.id,id=request.POST["id"]).delete()
            return redirect(dashboard)
        else:
            return render(request, "dashboard.html",{"pi":pers_info,"ei":edu_info,"ci":cert_info,"ti":tech_sk_info,"ai":aca_pr_info})
    except:
        return redirect(personal_information)

def personal_information(request):
    if(request.method == "GET"):
        if("uname" in request.session):
            return render(request,"personal_info.html",{})
        else:
            return redirect(login)
    
    else:
        p1=personal_info()
        
        fullname=request.POST['fullname']
        phone_number=request.POST['phone_number']
        Gender=request.POST['Gender']
        dob=request.POST['dob']
        emailid=request.POST['emailid']
        Address=request.POST['Address']
        hobbies=request.POST['hobbies']
        languages_known=request.POST['languages_known']
        linkedin=request.POST['linkedin']
        github=request.POST['github']
        objective=request.POST['objective']
        
        p1.fullname=fullname
        p1.phone_number=phone_number
        p1.Gender=Gender
        p1.dob=dob
        p1.emailid=emailid
        p1.Address=Address
        p1.hobbies=hobbies
        p1.languages_known=languages_known
        p1.linkedin=linkedin
        p1.github=github
        p1.objective=objective
        
        uname = request.session["uname"]
        user = User_Info.objects.get(username=uname)
        p1.user = user
        
        p1.save()

        #return redirect(fields)
        return render(request, 'dashboard.html',{"Pers":p1.id,"pi":p1})
    
   #testing purpose   
   
def educational_Details(request,Pers):
    if (request.method =="GET"):
        return render(request,"educational_details.html",{})  
    else:
        e1=educational_details()
        
        e1.nameOfExamination=request.POST['nameOfExamination']
        e1.institute=request.POST['institute']
        e1.university=request.POST['university']
        e1.percentage=request.POST['percentage']
        e1.yearOfcompletion=request.POST['yearOfcompletion']
        e1.perIn_id=personal_info.objects.get(id=Pers)
        
        e1.save()
        
        return redirect(dashboard)
    
        
def Certification(request,Pers):
    if (request.method =="GET"):
        return render(request,"Certification.html",{})  
    else:
        
        c1=certification()
        
        c1.certification=request.POST['certification']
        c1.perIn_id=personal_info.objects.get(id=Pers)
        
        c1.save()
         
        return redirect(dashboard)    
        
        
def Technical_Skills(request,Pers):
    if (request.method =="GET"):
        return render(request,"Technical_Skills.html",{})
    else:
        
        t1=technical_skills()
        
        t1.skills=request.POST['skills']
        t1.perIn_id=personal_info.objects.get(id=Pers)
        
        t1.save()
        
        return redirect(dashboard)
        
               
def Academic_Project(request,Pers):
    if (request.method =="GET"):
        return render(request,"Academic_Project.html",{})
    else:
        a1=academic_project()
        
        a1.project_name=request.POST['project_name']
        a1.project_title=request.POST['project_title']
        a1.technologies_used=request.POST['technologies_used']
        a1.description=request.POST['description']
        a1.perIn_id=personal_info.objects.get(id=Pers)
        
        a1.save()
        
        return redirect(dashboard)
    
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
        


from .process import html_to_pdf
from django.http import HttpResponse
from django.template.loader import render_to_string

#Creating a class based view
def generatePdf(request):

    uname = request.session["uname"]
    Pers=personal_info.objects.get(user=uname)
    Ed_d=educational_details.objects.filter(perIn_id=Pers.id)
    certi=certification.objects.filter(perIn_id=Pers.id)
    Tec_Skill=technical_skills.objects.filter(perIn_id=Pers.id)
    acd_p=academic_project.objects.filter(perIn_id=Pers.id)

    open('UserApp/templates/temp.html', "w").write(render_to_string('Resume.html', {"Ed_d":Ed_d,"certi":certi,"Tec_Skill":Tec_Skill,"acd_p":acd_p,"Pers":Pers}))

    # Converting the HTML template into a PDF file
    pdf = html_to_pdf('temp.html')
        
        # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')
