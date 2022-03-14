from curses.ascii import US
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class SkillsForm(ModelForm):
    class Meta:
        model = SkillCv
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class UserSkillForm(ModelForm):
    class Meta:
        model = UserSkills
        fields = ['skill', 'percentage']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1' , 'password2']