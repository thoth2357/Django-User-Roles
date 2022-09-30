from django.contrib import admin
from django.urls import path
from . import views as myviews

urlpatterns = [
    path('', myviews.signup, name='signup'),
    path('login/', myviews.login, name='login'),
    path('logout', myviews.logout, name='logout'),
    path('create-teachers/', myviews.PrincipalAddTeacher, name='create-teachers')  # type: ignore
]