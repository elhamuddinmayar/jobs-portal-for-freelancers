from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,UserRegistrationForm ,UserEditForm,ProfileEditForm,CompanyEditForm
from .models import Profile,Company,Job,Suggestions,Rating,RatingCompany
from django.contrib import messages
from django.contrib.auth.models import  User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#..............USER LOGIN............
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return redirect("home")

#.........LOGOUT...........
def logout_user(request):
    logout(request)
    return redirect("login")

#.........home...........
@login_required
def home(request):
    return render(request, "home.html", {'request':request})

#.........REGISTER...........
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            # return render(request,'account/register_done.html',{'new_user': new_user})
            messages.success(request, 'Successfully Registered')
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


#........EDIT PROFILE...............
@login_required
def edit(request):
    
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated ''successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,'account/edit.html',{'user_form': user_form,'profile_form': profile_form})
    return redirect("show_profile" ,request.user.id)

#.........Show Profile
@login_required
def show_profile(request,id):
    profile = get_object_or_404(Profile,user_id=id)
    my_rates=Rating.objects.filter(reciever=profile.user.first_name)
    my_rates_company=RatingCompany.objects.filter(reciever=profile.user.first_name)
    company=Company.objects.filter(id=request.user.id) 

    collection_rates=Rating.objects.filter(reciever=profile.user.first_name)
    rate_list=[]
    count=0
    for rate in collection_rates:
        count+=1
        rate_list.append(rate.rating_value)
    if not rate_list:
        sum_rates="No reviews given"
    else:
        num=sum(rate_list)/count
        sum_rates=round(num)
        
    
    
    return render(request, "account/profile.html", {'profile':profile,
                                                    "my_rates":my_rates,
                                                    "my_rates_company":my_rates_company,
                                                    "company":company,
                                                    "a_rates":sum_rates})
#..........Rate profile.................
@login_required
def rate_user(request,id):
    if request.method == "POST":
        giver = request.user
        reciever =Profile.objects.get(id=id)
        rating_value = request.POST['rating_value']
        comment= request.POST['comment']
        suggested_number_of=request.user.id
        rate = Rating(giver=giver,reciever=reciever.user.first_name,rating_value=rating_value,comment=comment,
                      suggested_number_of=suggested_number_of)
        if giver==request.user:
            rate.save()
            messages.success(request, f"You have successfully reviewed {reciever}")
            return redirect("show_profile",reciever.id)
    return render(request, 'account/give_rating.html')
#....................... Rate From Company...............
@login_required
def rate_company(request,id):
    if request.method == "POST":
        # giver = request.user
        company=Company.objects.get(id=request.user.id)
        reciever =Profile.objects.get(id=id)
        rating_value = request.POST['rating_value']
        comment= request.POST['comment']
        c_id=company.id
        rate = RatingCompany(giver=company.name,
                      reciever=reciever.user.first_name,
                      rating_value=rating_value,
                      comment=comment,
                      suggested_number_of=c_id)
        if c_id==company.id:
            rate.save()
            messages.success(request, f"You have successfully reviewed {reciever} form {company.name}")
            return redirect("show_profile",reciever.id)
    return render(request, 'account/give_rating_company.html')

#..........Show Poeple
@login_required
def show_people(request):
    people=Profile.objects.all()
    return render(request,"account/people.html",{"people":people})

#.............. Register Company
@login_required
def register_company(request):
    if request. method == 'POST':
        name = request.POST['name']
        profile_photo= request.FILES.get('profile_photo')
        background_photo = request.FILES.get('background_photo')
        location = request.POST['location']
        activity_scope = request.POST['activity_scope']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        website = request.POST['website']      
                
        if (len(name) >= 4) and (len(activity_scope) >= 2) and ("@" in email):
            company = Company(user=request.user, name=name, location=location,
                              profile_photo=profile_photo,
                              background_photo=background_photo,
                              activity_scope=activity_scope,
                                email=email, phone_number=phone_number, 
                                website=website)
        
            company.save()
            messages.success(request, "Company successfully registered")
            
            return redirect("show_company",request.user.id)
        else:
            messages.error(request, "There was an error with the form!")
    return render(request, 'account/company_register.html')

#..............Show Company...........
@login_required
def show_company(request,id):
    company = get_object_or_404(Company,user_id=id)
    relate_jobs=Job.objects.filter(company_id=request.user.company.id)
    return render(request, "account/company.html", {'company':company,"relate_jobs":relate_jobs})

#..............Edit Company...........

@login_required
def editcompany(request):
   
    if request.method == 'POST':
        
        company_form = CompanyEditForm(instance=request.user.company,data=request.POST,files=request.FILES)
        if  company_form.is_valid():
            company_form.save()
            messages.success(request, 'Company Successfully Updated !')
        else:
            messages.error(request, 'Error Updating Your Profile')
    else:
        profile_form = CompanyEditForm(instance=request.user.profile)
        return render(request,'account/edit_company.html',{'company_form': profile_form})
    return redirect("show_company" ,request.user.id)

#............ Announce Job.............
@login_required
def announce_job(request):
    if request. method == 'POST':
        title = request.POST['title']
        salary = request.POST['salary']
        agreement_duration = request.POST['agreement_duration']
        gender = request.POST['gender']
        education = request.POST['education']
        required_experience = request.POST['required_experience']
        end_of_convenant = request.POST['end_of_convenant']    
        location = request.POST['location']    
                
        if (len(title) >= 1):
            company=Company.objects.get(user=request.user)
            job = Job(title=title, company=company, salary=salary,
                              agreement_duration=agreement_duration,
                              gender=gender,
                              education=education,
                                required_experience=required_experience, end_of_convenant=end_of_convenant, 
                                location=location)
        
            job.save()
            messages.success(request, "Company successfully registered")
            return redirect("jobs")
        else:
            messages.error(request, "There was an error with the form!")
    return render(request, 'account/announce_job.html')

@login_required
def job_list(request):
    jobs = Job.objects.all()
    paginator = Paginator(jobs, 8)
    page_number = request.GET.get("page", 1)
    
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,"account/jobs.html",{"posts":posts})
   
#................Job details.............
@login_required
def job_details(request,id):
    job = Job.objects.get(id=id)
    return render(request, 'account/jobs_details.html', {'job':job})


def unauthorized_access(request):
    return render(request, 'account/unauthorized.html', status=403)


@login_required
def apply_job(request,id):
    job=Job.objects.get(id=id)
    if request. method == 'POST':
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        interests = request.POST['interests']
        languages = request.POST['languages']
        work_experience = request.POST['work_experience']
        education_background = request.POST['education_background']
        personal_skills = request.POST['personal_skills']    
        
        user=User.objects.get(id=request.user.id)
        apply = Suggestions(suggested_user=user,job=job,phone_number=phone_number, address=address, interests=interests,
                            languages=languages,
                            work_experience=work_experience,
                            education_background=education_background,
                            personal_skills=personal_skills)
        
        apply.save()
        messages.success(request, "Apply was successfull !")
        return redirect("jobs")
    
    return render(request, 'account/apply_job.html',{"job":job})
       
@login_required
def suggestions(request,id):
    jobs=Job.objects.filter(company_id=id)
    suggestion_count=[]
    
    for job in jobs:
        count=Suggestions.objects.filter(job_id=job.id).count()
        suggestion_count.append((job,count))
    
    return render(request,"account/suggestions.html",{"suggestion_count":suggestion_count})

@login_required
def view_suggestion(request,id): 
    suggestion = Suggestions.objects.filter(job_id=id)
    return render(request,"account/view_suggestion.html",{"suggestion":suggestion})

@login_required
def suggestion_details(request,id):
    
    suggestion_details=Suggestions.objects.get(id=id)
    return render(request,"account/suggestion_details.html",{"sug":suggestion_details})

@login_required
def delete_job(request,id):
    obj=Job.objects.get(id=id)
    obj.delete()
    messages.success(request,"Job successfully deleted")
    # return render(request,"account/suggestions.html")
    return redirect("suggestions", request.user.company.id)

@login_required 
def delete_suggestion(request,id):
    
    obj=Suggestions.objects.get(id=id)
    obj.delete()
    messages.success(request,"Suggestion successfully deleted")
    # return render(request,"account/suggestions.html")
    return redirect("view_suggestion",obj.job_id)

@login_required
def all_user(request):
    users=Profile.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get("page", 1)
    
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,"account/users.html",{"posts":posts})
    

@login_required
def search_user(request):
    query=request.GET.get("q","")
    users_find=User.objects.filter(username__icontains=query)
    user=User.objects.get(username=query)
    profile=Profile.objects.get(id=user.id)
    return render(request,"account/search.html",{"query":query,"users_find":users_find,"profile":profile})

@login_required
def search_jobs(request):
    query=request.GET.get("q","")
    jobs_find=Job.objects.filter(title__icontains=query)
    return render(request,"account/search.html",{"query":query,"jobs_find":jobs_find})


@login_required
def manage_user_rates(request):
    profile=Profile.objects.get(id=request.user.id)
    rates=Rating.objects.filter(reciever=profile.user.first_name)
    return render(request,"account/manage_user_rate.html",{"rates":rates})



@login_required
def manage_company_rates(request):
    profile=Profile.objects.get(id=request.user.id)
    rates=RatingCompany.objects.filter(reciever=profile.user.first_name)
    return render(request,"account/manage_company_rate.html",{"rates":rates})

@login_required
def delete_user_rates(request,id):
    obj=Rating.objects.get(id=id)
    obj.delete()
    messages.success(request,"Actions successfully Done!")
    return redirect("manage_user_rates")

@login_required
def delete_company_rates(request,id):
    obj=RatingCompany.objects.get(id=id)
    obj.delete()
    messages.success(request,"Actions successfully Done!")
    return redirect("manage_company_rates")

