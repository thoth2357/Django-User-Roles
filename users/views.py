import email
import re
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as user_login, logout

from .models import Student, TeacherDetails, User, StudentDetails
from .forms import SignupForm,TeacherCreateForm
from .permissions import is_principal

# Create your views here.
def signup(request):
    form = SignupForm(request.POST)
    context = {
        'form': form,
    }
    #validating forms
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user_type = form.cleaned_data['user_type']
        
        new_user = User.objects.create_user(email=email, password=password, type=user_type)
        StudentDetails.objects.create(user=new_user)
        return HttpResponse("Success")
    return render(request, 'signup.html', context)

def login(request):
    '''
    Login View
    '''
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None:
                user_login(request, authenticated_user) # login the authenticated user
                
                user_type = User.objects.get(email=authenticated_user).type
                if authenticated_user.is_authenticated and user_type == 'STUDENT':
                    return HttpResponse(f"Welcome Student. your email for login is {authenticated_user.email}")
                elif authenticated_user.is_authenticated and user_type == 'TEACHER':
                    return HttpResponse(f"Welcome Teacher. your email for login is {authenticated_user.email} ")
                elif authenticated_user.is_authenticated and user_type == 'PRINCIPAL':
                    return HttpResponse(f"Welcome Principal. your email for login is {authenticated_user.email} ")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
        
@user_passes_test(is_principal)
def PrincipalAddTeacher(request):
    '''
    View for principal to add teachers
    '''
    form = TeacherCreateForm(request.POST)
    context = {
        'form': form,
    }
    if form.is_valid():
        # try:
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = 'TEACHER'
            Students = form.cleaned_data['Students']
            new_user = User.objects.create_user(email=email, password=password, type=user_type)
            new_teacher_details = TeacherDetails(user=new_user)
            new_teacher_details.save()
            for student in Students:
                new_teacher_details.Students.add(User.objects.get(id=student.id).id)
            new_teacher_details.save()
            return HttpResponse("Success")
            # return HttpResponse("Error",e)
    return render(request, 'create-teachers.html', context)
    
def logout(request):
    '''
    Logout View
    '''
    logout(request)
    return redirect('signup')