import email
from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, TeacherDetails, User, StudentDetails

from .forms import SignupForm,TeacherCreateForm

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
            print(Students, 'test', [student.id for student in Students])
            new_teacher_details.Students.set([student.id for student in Students])
            return HttpResponse("Success")
            # return HttpResponse("Error",e)
    return render(request, 'create-teachers.html', context)
    
