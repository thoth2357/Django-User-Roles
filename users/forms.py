from django import forms
from .models import User

class SignupForm(forms.Form):
    email = forms.CharField(label="Enter EMail", max_length=100)
    password = forms.CharField(label="Enter Password", widget = forms.PasswordInput())
    user_type = forms.ChoiceField(label="Choose your login type", choices = User.Types.choices)
    

class TeacherCreateForm(forms.Form):
    email = forms.CharField(label="Enter Teacher Email", max_length=100)
    password = forms.CharField(label="Enter Password For Teacher", widget = forms.PasswordInput())
    Students = forms.ModelMultipleChoiceField(label="Select Students", queryset=User.objects.all().filter(type='STUDENT'))



