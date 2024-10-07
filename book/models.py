from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import datetime
from PIL import Image

import os

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True, default='default.jpg')
    year_of_admission = models.IntegerField(choices=[(year, year) for year in range(2017, datetime.date.today().year + 1)], default=2017)
    can_post = models.BooleanField(default=False)
    accept_log = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call original save method first

        try:
            # Access the path of the uploaded image
            image_path = self.profile_picture.path

            with Image.open(image_path) as img:
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)

                    # Create a new filename to avoid overwriting
                    new_filename, extension = os.path.splitext(image_path)
                    new_filename = f"{new_filename}_compressed{extension}"

                    # Save the resized image to a new file
                    img.save(new_filename)

        except FileNotFoundError:  # Handle potential file not found errors
            pass

    


class Moreinfo(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    nick_name = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)  # Use URLField instead of CharField for validation

    # Validate phone number using a regular expression
    phone_regex = RegexValidator(regex=r"^\d{10,15}$", message="Phone number must be 10-15 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    instagram_handle = models.CharField(max_length=50, blank=True)  # Use "handle" for clarity

    def __str__(self):
        return f"{self.student.user.username}'s More Info"  # More informative string representation

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_year = models.IntegerField(choices=[(year, year) for year in range(2017, datetime.date.today().year + 1)], default=2017)
    event_date = models.DateField()
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images')

class EventImages(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='event_images')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call original save method first

        try:
            # Access the path of the uploaded image
            image_path = self.image.path

            with Image.open(image_path) as img:
                if img.height > 500 or img.width > 500:
                    output_size = (500, 350)
                    img.thumbnail(output_size)

                    # Create a new filename to avoid overwriting
                    new_filename, extension = os.path.splitext(image_path)
                    new_filename = f"{new_filename}_compressed{extension}"

                    # Save the resized image to a new file
                    img.save(new_filename)

        except FileNotFoundError:  # Handle potential file not found errors
            pass
