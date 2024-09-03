from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    try:
        form = UserCreationForm()
        return render(request, 'users/register.html',{'form':form})
    except UserCreationForm.DoesNotExist:
        return render(request, "404.html")