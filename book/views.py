from .models import Event, EventImage
from django.shortcuts import render, redirect
#from django.contrib.auth.models
from django.contrib.auth.models import User  # Or your custom user model
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import AuthenticationForm   

#from django.http import HttpResponse





# Create your views here.




def home(request):
    try:
        events = Event.objects.all()
        event_data = [(event, EventImage.objects.filter(event=event)) for event in events]
        context = {"event_data": event_data}
        return render(request, 'yb-base.html', context)
    except Event.DoesNotExist:
        return render(request, "404.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Data validation (improve as needed)
        if not username or not password:
            errors = ["Please fill in all required fields."]
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace with your desired success page
            else:
                errors = ["Invalid credentials."]

    return render(request, 'login.html', {'errors': errors})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Data validation (improve as needed)
        if not username or not email or not password1 or not password2:
            errors = ["Please fill in all required fields."]
        elif password1 != password2:
            errors = ["Passwords do not match."]
        elif User.objects.filter(username=username).exists():
            errors = ["Username already exists."]
        else:
            # Create user and handle errors (consider using try-except)
            try:
                user = User.objects.create_user(username, email, password1)
                login(request, user)
                return redirect('login')  # Redirect to success page
            except Exception as e:
                errors = [f"Registration failed: {str(e)}"]

        return render(request, 'register.html', {'errors': errors})
    else:
        return render(request, 'register.html')