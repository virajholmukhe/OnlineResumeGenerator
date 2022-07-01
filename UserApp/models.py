from django.db import models

# Create your models here.
class User_Info(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "userInfo"
        
class personal_info(models.Model):
    fullname= models.CharField(max_length=20)
    phone_number=models.CharField(max_length=10)
    Gender=models.CharField(max_length=6)
    dob=models.DateField(auto_now=False,auto_now_add=False)
    emailid=models.EmailField(max_length=50)
    Address=models.TextField(max_length=225)
    hobbies=models.CharField(max_length=100)
    languages_known=models.CharField(max_length=50)
    linkedin=models.CharField(max_length=200)
    github=models.CharField(max_length=200)
    objective=models.TextField(max_length=1000)
    user = models.ForeignKey(User_Info, on_delete=models.CASCADE)
    
    class Meta:
        db_table="personal_info"
    
class my_resumes(models.Model):
    user = models.ForeignKey(User_Info, on_delete=models.CASCADE)
    person_info = models.ForeignKey(personal_info, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes')
    
    
    class Meta:
        db_table="my_resumes"
    
class educational_details(models.Model):
    nameOfExamination = models.CharField(max_length=50)
    institute=models.CharField(max_length=500)
    university=models.CharField(max_length=100)
    percentage=models.CharField(max_length=10)
    yearOfcompletion=models.CharField(max_length=10)
    perIn_id = models.ForeignKey(personal_info,on_delete=models.CASCADE)

    class Meta:
        db_table="educational_details"
    
class certification(models.Model):
    certification=models.CharField(max_length=100)
    perIn_id= models.ForeignKey(personal_info,on_delete=models.CASCADE)

    class Meta:
        db_table="certification"
        
   
class technical_skills(models.Model):
    skills= models.CharField(max_length=100)
    perIn_id = models.ForeignKey(personal_info,on_delete=models.CASCADE)
    
    class Meta:
        db_table="technical_skills"
        
class academic_project(models.Model):
    project_name= models.CharField(max_length=100)
    project_title= models.CharField(max_length=100)
    technologies_used=models.CharField(max_length=200)
    description=models.TextField(max_length=1000)
    perIn_id= models.ForeignKey(personal_info,on_delete=models.CASCADE)
    
    class Meta:
        db_table="academic_project"
    
class ContactMe(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table="ContactMe"
    
    
    