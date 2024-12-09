from django.db import models
from django.conf import settings
from django.utils.text import slugify
import datetime
from django.urls import reverse


class Company(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=250,blank=True,null=True)
    profile_photo=models.ImageField(upload_to="company_profile",blank=True,null=True)
    background_photo=models.ImageField(upload_to="company_background",blank=True,null=True)
    location = models.CharField(max_length=250,blank=True,null=True)
    activity_scope = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(max_length=250, unique=True,blank=True,null=True)
    phone_number = models.CharField(max_length=50,blank=True,null=True)
    website = models.URLField(max_length=250, null=True,blank=True)
    established_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-established_at']
        indexes = [
            models.Index(fields=['-established_at'])
        ]
    
    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    # info   
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_photo=models.ImageField(upload_to="images",blank=True,null=True)
    bio=models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    social_media_link = models.URLField(blank=True)
    interests = models.CharField(max_length=255,null=True,blank=True)
    languages = models.CharField(max_length=255, blank=True)  # Comma-separated
    work_experience = models.CharField(max_length=255, blank=True)
    education_background = models.CharField(max_length=255, blank=True)
    personal_skills = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
  
        
    
class Job(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', 'M'
        FEMALE = 'Female', 'F'
    
    title = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    slug = models.SlugField()
    salary = models.IntegerField()
    agreement_duration = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    education = models.CharField(max_length=20,null=True,blank=False)
    required_experience = models.CharField(max_length=250, null=True, blank=True)
    end_of_convenant = models.DateField()
    announced_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=250, blank=True)
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    

class Suggestions(models.Model):
    suggested_user=models.CharField(max_length=255)
    job=models.ForeignKey(Job, on_delete=models.CASCADE, related_name='announced_jobs')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    interests = models.CharField(max_length=255,null=True,blank=True)
    languages = models.CharField(max_length=255, blank=True,null=True)  
    work_experience = models.CharField(max_length=255, blank=True)
    education_background = models.CharField(max_length=255, blank=True)
    personal_skills = models.CharField(max_length=255, blank=True)
    submit_time=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.job.title}'
    
    
class Rating(models.Model):
    u_c_id=models.IntegerField(name="suggested_number_of")
    giver=models.CharField(max_length=255,name="giver")
    reciever=models.CharField(max_length=255,name="reciever")
    rating_value=models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.giver} rated {self.reciever}"
    
class RatingCompany(models.Model):
    u_c_id=models.IntegerField(name="suggested_number_of")
    giver=models.CharField(max_length=255,name="giver")
    reciever=models.CharField(max_length=255,name="reciever")
    rating_value=models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.giver} rated {self.reciever}"