from django import forms
from django.contrib.auth.models import User
from .models import Profile,Company,Job,Rating



class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)  
    widgets = {
            'username': forms.TextInput(attrs={'class':'form-control',"placeholder":"Username"}),
            'password': forms.Select(attrs={'class':'form-control'})
            
        }
       
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name',"last_name", 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
    widgets = {
            'username': forms.TextInput(attrs={'class':'form-control',"placeholder":"Username"}),
            'first_tname': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control'}),
            
        }

    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        def clean_email(self):
            data = self.cleaned_data['email']
            qs = User.objects.exclude(id=self.instance.id).filter(email=data)
            if qs.exists():
                raise forms.ValidationError(' Email already in use.')
            return data
        
    widgets = {
            
        'first_tname': forms.TextInput(attrs={'class':'form-control'}),
        'last_name': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),        
        }
    

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_photo","bio","phone_number","address","social_media_link","interests","languages","work_experience","education_background","personal_skills"]
    widgets = {
        'profile_photo': forms.FileInput(attrs={'class':'form-control',"placeholder":"Username"}),
        'bio': forms.TextInput(attrs={'class':'form-control'}),
        'phone_number': forms.NumberInput(attrs={'class':'form-control'}),
        'address': forms.TextInput(attrs={'class':'form-control'}),
        'social_media_link': forms.URLInput(attrs={'class':'form-control'}),
        'interests': forms.TextInput(attrs={'class':'form-control'}),
        'languages': forms.TextInput(attrs={'class':'form-control'}),
        'work_experience': forms.NumberInput(attrs={'class':'form-control'}),
        'education_background': forms.TextInput(attrs={'class':'form-control'}),
        'personal_skills': forms.TextInput(attrs={'class':'form-control'}), 
        }


class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name","profile_photo","background_photo","location","activity_scope","email","phone_number","website"]
        
    widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'profile_photo': forms.FileInput(attrs={'class':'form-control'}),
        'background_photo': forms.FileInput(attrs={'class':'form-control'}),
        'location': forms.TextInput(attrs={'class':'form-control'}),
        'activity_scope': forms.TextInput(attrs={'class':'form-control'}),
        'email': forms.EmailInput(attrs={'class':'form-control'}),
        'phone_number': forms.TextInput(attrs={'class':'form-control'}),
        'website': forms.URLInput(attrs={'class':'form-control'}),
        }
#............... Job Form...................
class JobForm(forms.ModelForm):
    
    class Meta:
        model = Job
        fields = ('title', 'company', 'salary', 'agreement_duration',
                  'gender', 'education', 'required_experience', 'end_of_convenant',"location")
        
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.Select(attrs={'class':'form-control'}),
            'salary': forms.NumberInput(attrs={'class':'form-control'}),
            'agreement_duration': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-select'}),
            'education': forms.Select(attrs={'class':'form-select'}),
            'required_experience': forms.TextInput(attrs={'class':'form-control'}),
            'end_of_convenant': forms.DateInput(attrs={'class':'form-control'}),
            'location': forms.DateInput(attrs={'class':'form-control'}),
            
            }
        
# class RatingForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ("giver","reciever","rating_value", "comment")
        
    
