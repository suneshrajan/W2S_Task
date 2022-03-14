from django.shortcuts import render
from django.http import HttpResponse

from .models import *
import pandas as pd
# Create your views here.


def home(request):
	# group_obj = Group.objects.get(name="Employee")
	user_obj = User.objects.filter()
	employee_obj = user_obj.filter(groups__name="Employee")
	skill_list = SkillCv.objects.all().order_by('id')
	user_skils = UserSkills.objects.filter(user=employee_obj)
	user_skill_df = pd.DataFrame(list(UserSkills.objects.filter(user__groups__name="Employee").values_list('user_id', 'user__first_name', 'user__last_name', 'user__email', 'user__last_login', 'skill__name', 'percentage')), columns=['user_id', 'first_name', 'last_name', 'email', 'last_loggedin', 'skill', 'percentage'])
	users_with_skills = user_skill_df.groupby('user_id').apply(lambda x:x.to_dict('r')).to_dict()
	datas = {
		'users_with_skills': users_with_skills,
		'skills': skill_list,
		'total_users': user_obj.filter(groups__name__in=['Manager', 'Employee']).count(),
		'managers': user_obj.filter(groups__name__in=['Manager']).count(),
		'employees': employee_obj.count()
		}
	return render(request, 'task/dashboard.html', datas)

def employee(request, user_id):
	user_obj = User.objects.get(id=user_id)
	return render(request, 'task/employee.html')
