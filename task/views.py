from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def say_hi(request) :
    print("hi")
    context = {
        "name": "Sunesh Rajan",
    }
    return render(request, "index.html", context)
