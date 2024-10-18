from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import Student

class StudentUpdateForm(forms.ModelForm):

    class Meta:
        model=Student
        fields=['first_name','last_name','profile_picture','year_of_admission']

class fullStudentUpdateForm(forms.ModelForm):

    class Meta:
        model=Student
        fields=['first_name','last_name','phone_number','linkedin_url','instagram_handle',
                'nick_name','year_of_admission','profile_picture']