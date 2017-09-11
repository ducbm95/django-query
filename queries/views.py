import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

def index(request):
    return render(request, 'queries/index.html', {})
