import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import context

from .models import *
import pandas as pd
from .forms import CreateUserForm, SkillsForm, UserForm, UserSkillForm
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def regiser(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')

				user_obj = User.objects.get(username=user)
				group = Group.objects.get(name='Employee')
				user_obj.groups.add(group)

				for skill in SkillCv.objects.all():
					UserSkills.objects.create(user=user_obj, skill=skill, percentage=0)

				messages.success(request, 'Account Successfuly Created ' + user)
				return redirect('login')
		context = {'form' : form}
		return render(request, 'task/register.html', context)


def authenticate_user(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, "Username OR Password is incorret !!!")
		context = {}
		return render(request, 'task/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
	# group_obj = Group.objects.get(name="Employee")
	user_obj = User.objects.filter()
	employee_obj = user_obj.filter(groups__name="Employee")
	skill_list = SkillCv.objects.all().order_by('id')
	user_skils = UserSkills.objects.filter(user=employee_obj)
	
	group_name = User.objects.filter(id=request.user.id).values_list('groups__name',flat=True)[0]
	if group_name == 'Employee':
		user_skill_df = pd.DataFrame(list(UserSkills.objects.filter(user_id=request.user.id).values_list('user_id', 'user__first_name', 'user__last_name', 'user__email', 'user__last_login', 'skill__name', 'percentage')), columns=['user_id', 'first_name', 'last_name', 'email', 'last_loggedin', 'skill', 'percentage']).fillna('')
	else:
		user_skill_df = pd.DataFrame(list(UserSkills.objects.filter(user__groups__name="Employee").values_list('user_id', 'user__first_name', 'user__last_name', 'user__email', 'user__last_login', 'skill__name', 'percentage')), columns=['user_id', 'first_name', 'last_name', 'email', 'last_loggedin', 'skill', 'percentage']).fillna('')

	
	users_with_skills = user_skill_df.groupby('user_id').apply(lambda x:x.to_dict('r')).to_dict()
	datas = {
		'users_with_skills': users_with_skills,
		'skills': skill_list,
		'total_users': user_obj.filter(groups__name__in=['Manager', 'Employee']).count(),
		'managers': user_obj.filter(groups__name__in=['Manager']).count(),
		'employees': employee_obj.count(),
		'group_name' : group_name
		}

	return render(request, 'task/dashboard.html', datas)


@login_required(login_url='login')
def employee(request, user_id):
	user_skill_dict = pd.DataFrame(list(UserSkills.objects.filter(user_id=user_id).order_by('skill_id').values_list('id', 'skill__name', 'percentage')),columns=['skill_id', 'skill', 'percentage']).to_dict('r')
	group_name = User.objects.filter(id=request.user.id).values_list('groups__name',flat=True)[0]
	context = {
		'skill_list' : user_skill_dict,
		'employee' : User.objects.get(id=user_id),
		'group_name' : group_name
	}
	return render(request, 'task/employee.html', context)


@login_required(login_url='login')
def create_skills(request):
	form = SkillsForm()
	if request.method == 'POST':
		form = SkillsForm(request.POST)
		if form.is_valid():
			if not SkillCv.objects.filter(name=form.cleaned_data['name']).exists():
				skll_obj = SkillCv()
				skll_obj.name = form.cleaned_data['name']
				skll_obj.save()

				employee_obj = User.objects.filter(groups__name="Employee")
				for employee in employee_obj:
					UserSkills.objects.create(user=employee, skill=skll_obj, percentage=0)
			else:
				print("Skill Already Exists !")
			return redirect('/')

	context = {'form': form}

	return render(request, 'task/skill_form.html', context)


@login_required(login_url='login')
def update_skills(request, skill_id):
	skill_obj = SkillCv.objects.get(id=skill_id)
	form = SkillsForm(instance=skill_obj)

	if request.method == 'POST':
		form = SkillsForm(request.POST, instance=skill_obj) 
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form': form}

	return render(request, 'task/skill_form.html', context)


@login_required(login_url='login')
def delete_skills(request, skill_id):
	skill_obj = SkillCv.objects.get(id=skill_id)

	if request.method == 'POST':
		skill_obj.delete()
		return redirect('/')
	context = {'skill':skill_obj}

	return render(request, 'task/delete_skill.html', context)


@login_required(login_url='login')
def create_employee(request):
	form = UserForm()
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			if not User.objects.filter(username=form.cleaned_data['username']).exists():
				form.save()
				user = form.cleaned_data.get('username')
				
				user_obj = User.objects.get(username=user)
				group = Group.objects.get(name='Employee')
				user_obj.groups.add(group)

				for skill in SkillCv.objects.all():
					UserSkills.objects.create(user=user_obj, skill=skill, percentage=0)
			else:
				print("Skill Already Exists !")
			return redirect('/')

	context = {'form': form}

	return render(request, 'task/user_form.html', context)


@login_required(login_url='login')
def update_employee(request, user_id):
	user_obj = User.objects.get(id=user_id)
	form = UserForm(instance=user_obj)

	if request.method == 'POST':
		form = UserForm(request.POST, instance=user_obj) 
		if form.is_valid():
			form.save()
			group_name = User.objects.filter(id=request.user.id).values_list('groups__name',flat=True)[0]
			if group_name == 'Employee':
				return redirect('/employee/'+str(user_obj.id))
			else:
				return redirect('/')

	context = {'form': form}

	return render(request, 'task/skill_form.html', context)


@login_required(login_url='login')
def delete_employee(request, user_id):
	user_obj = User.objects.get(id=user_id)

	if request.method == 'POST':
		user_obj.delete()
		return redirect('/')
	context = {'user':user_obj}

	return render(request, 'task/delete_employee.html', context)


@login_required(login_url='login')
def update_employee_skill(request, user_skill_id):

	user_skill_obj = UserSkills.objects.get(id=user_skill_id)
	form = UserSkillForm(instance=user_skill_obj)

	if request.method == 'POST':
		form = UserSkillForm(request.POST, instance=user_skill_obj) 
		if form.is_valid():
			form.save()
			return redirect('/employee/'+str(user_skill_obj.user_id))

	context = {'form': form}
	
	return render(request, 'task/user_skill_form.html', context)


@login_required(login_url='login')
def delete_employee_skill(request, user_skill_id):
	user_skill_obj = UserSkills.objects.get(id=user_skill_id)

	if request.method == 'POST':
		user_skill_obj.percentage = 0
		user_skill_obj.save()
		return redirect('/employee/'+str(user_skill_obj.user_id))
	context = {'user_skill':user_skill_obj}

	return render(request, 'task/delete_user_skill.html', context)


@login_required(login_url='login')
def manager_profile(request):
	user_obj = User.objects.get(id=request.user.id)
	context = {'manager':user_obj}
	return render(request, 'task/manager_profile.html', context)
