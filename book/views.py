from .models import Event, EventImage, Student
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Or your custom user model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required as lr
from .forms import StudentUpdateForm, fullStudentUpdateForm
#from django.contrib.auth.models
#from django.contrib.auth.forms import AuthenticationForm   
import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentUpdateForm

current_year = datetime.date.today().year
message=[]



@lr
def profile_view(request):
    if request.method == 'POST':
        s_form = StudentUpdateForm(request.POST, request.FILES, instance=request.user.student)
        if s_form.is_valid():
            student = s_form.save()  # Update the existing student object
            message.append('Wait to be accepted into the system you would recievce an Email shortly')
            return redirect('message')
    else:
        s_form = StudentUpdateForm(instance=request.user.student)
    context = {'s_form': s_form}
    return render(request, 'profile.html', context)

@lr
def full_profile_view(request):
    if request.method == 'POST':
        s_form = fullStudentUpdateForm(request.POST, request.FILES, instance=request.user.student)
        if s_form.is_valid():
            student = s_form.save()  # Update the existing student object
            message.append('profile updated')
            return redirect('fprofile')
    else:
        s_form = fullStudentUpdateForm(instance=request.user.student)
    context = {'s_form': s_form, 'error':message}
    return render(request, 'fprofile.html', context)

def main_view(request):
    year=current_year
    try:
        students = Student.objects.filter(year_of_admission=year)
        events = Event.objects.filter(event_year=year)
        event_data = [(event, EventImage.objects.filter(event=event)) for event in events]
        context = {'students': students,"event_data": event_data,'current_year':year}
        return render(request, 'yb-base.html', context)
    except Event.DoesNotExist:
        return render(request, "404.html")

@lr
def home_view(request):
    year=request.user.student.year_of_admission
    try:
        students = Student.objects.filter(year_of_admission=year)
        events = Event.objects.filter(event_year=year)
        event_data = [(event, EventImage.objects.filter(event=event)) for event in events]
        context = {'students': students, "event_data": event_data}
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
                    if user.student.accept_log is True:
                        login(request, user)
                        return redirect('home')  # Redirect to the home page after login
                    else:
                        errors.append("WAIT TO BE ACCEPTED")
                else:
                    errors.append("Invalid email or password.")
            except User.DoesNotExist:
                errors.append("No user with this email found.")

    # If it's a GET request or if there are errors, render the login page
    return render(request, 'login.html', {'errors': errors})

def register_view(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Data validation (improve as needed)
        if not username or not email or not password1 or not password2:
            errors.append("Please fill in all required fields.")
        elif password1 != password2:
            errors.append("Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        else:
            # Create user and handle errors (using try-except)
            try:
                user = User.objects.create_user(username, email, password1)
                login(request, user)  # Log in the newly created user

                # Redirect to login page only if user creation and login succeed
                return redirect('profile')
            except Exception as e:
                errors.append(f"Registration failed: {str(e)}")

    return render(request, 'register.html', {'errors': errors})

@lr
def logout_view(request):

    logout(request)
    return redirect('main')  # Redirect to the login page after logging out

def year_view(request, year=None):
    yeas = [yea for yea in range(2017, current_year + 1)]  # List of years

    if year is None:
        # Set default year to the current year
        year = datetime.date.today().year

    try:
        # Convert year from URL to integer (handle potential errors)
        year = int(year)
    except ValueError:
        # Display error message if year is not an integer
        return render(request, 'error.html', {'error_message': 'Invalid year provided.'})

    # Filter students based on the requested year
    students = Student.objects.filter(year_of_admission=year)

    context = {'students': students, 'requested_year': year, 'yeas': yeas,'current_year':current_year}
    return render(request, 'year.html', context)

def event_view(request, year=None):
    yeas = [yea for yea in range(2017, current_year + 1)]  # List of years


    if year is None:
        # Set default year to the current year
        year = datetime.date.today().year

    try:
        # Convert year from URL to integer (handle potential errors)
        year = int(year)
    except ValueError:
        # Display error message if year is not an integer
        return render(request, 'error.html', {'error_message': 'Invalid year provided.'})

    students = Student.objects.filter(year_of_admission=year)
    events = Event.objects.filter(event_year=year)
    event_data = [(event, EventImage.objects.filter(event=event)) for event in events]

    context = {'students': students, 'requested_year': year, 'yeas': yeas, "event_data": event_data, 'current_year':current_year}
    return render(request, 'event.html', context)

def message_view(request):
        context = {'message':message}
        return render(request, 'message.html', context)

def about_us_view(request):
        
        context = { 'current_year':current_year}
        return render(request, 'about_us.html', context)

from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Student

def detail_view(request, pk=None):
    try:
        pk = int(pk)
    except (TypeError, ValueError):
        return render(request, 'error.html', {'message': 'Invalid student ID'})
    
    # Fetch the student object, return 404 if not found
    student_info = get_object_or_404(Student, pk=pk)
    use = get_object_or_404(User, student=student_info)


    # Prepare the context with student data and current year
    context = {
        'student': student_info,
        'current_year': current_year,
        'use':use,
    }
    
    return render(request, 'detail.html', context)
