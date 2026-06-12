# from django.http import HttpResponse
from django.shortcuts import render
from pathlib import Path
from django.conf import settings

def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')
