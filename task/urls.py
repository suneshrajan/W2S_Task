from unicodedata import name
from . import views
from django.urls import path


urlpatterns = [
    path('register/',  views.regiser, name='register'),
    path('login/',  views.authenticate_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name="home"),
    path('employee/<str:user_id>/', views.employee, name='employee'),
    # create employees
    path('create/employee/', views.create_employee, name='create_employee'),
    path('update/employee/<str:user_id>', views.update_employee, name='update_employee'),
    path('delete/employee/<str:user_id>', views.delete_employee, name='delete_employee'),
    # create skills
    path('create/skills/', views.create_skills, name='create_skills'),
    path('update/skills/<str:skill_id>/', views.update_skills, name='update_skills'),
    path('delete/skills/<str:skill_id>/', views.delete_skills, name='delete_skills'),
    # skills & user map
    path('update/user/skill/<str:user_skill_id>/', views.update_employee_skill, name='update_employee_skill'),
    path('delete/user/skill/<str:user_skill_id>/', views.delete_employee_skill, name='delete_employee_skill'),
    # manager profile
    path('manager/profile/', views.manager_profile, name='manager_profile'),
]