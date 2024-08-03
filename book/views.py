from django.shortcuts import render
#from django.http import HttpResponse
#from 
# Create your views here.

def home(request):
    return render(request, 'yb-base.html')