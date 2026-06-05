# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse("Welcome to the homepage!")
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# def register(request):
#     return render(request, 'register.html')