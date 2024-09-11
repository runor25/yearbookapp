from .models import Event, EventImage, Student
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Or your custom user model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required as lr

#from django.contrib.auth.models
#from django.contrib.auth.forms import AuthenticationForm   



def main_view(request):
    try:
        events = Event.objects.all()
        event_data = [(event, EventImage.objects.filter(event=event)) for event in events]
        context = {"event_data": event_data}
        return render(request, 'yb-base.html', context)
    except Event.DoesNotExist:
        return render(request, "404.html")

@lr
def home_view(request):
    try:
        events = Event.objects.all()
        event_data = [(event, EventImage.objects.filter(event=event)) for event in events]
        context = {"event_data": event_data}
        return render(request, 'my_page.html', context)
    except Event.DoesNotExist:
        return render(request, "404.html")




def login_view(request):
    errors = []  # Initialize the errors list

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Data validation
        if not email:
            errors.append("Email is required.")
        if not password:
            errors.append("Password is required.")

        if not errors:
            try:
                # Get the user by email
                user = User.objects.get(email=email)
                # Authenticate the user using the username (email won't work directly in authenticate)
                user = authenticate(username=user.username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to the home page after login
                else:
                    errors.append("Invalid email or password.")
            except User.DoesNotExist:
                errors.append("No user with this email found.")

    # If it's a GET request or if there are errors, render the login page
    return render(request, 'login.html', {'errors': errors})

def register_view(request):
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

def logout_view(request):
    logout(request)
    return redirect('main')  # Redirect to the login page after logging out