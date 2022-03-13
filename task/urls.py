from unicodedata import name
from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('employee/', views.employee, name="employee")
]