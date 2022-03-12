from unicodedata import name
from . import views
from django.urls import path


urlpatterns = [
    path('say/hi/', views.say_hi, name="hi")
]