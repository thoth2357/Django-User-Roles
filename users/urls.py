from django.contrib import admin
from django.urls import path
from . import views as myviews

urlpatterns = [
    path('', myviews.signup, name='signup'),
    path('create-teachers/', myviews.PrincipalAddTeacher, name='create-teachers')  # type: ignore
]