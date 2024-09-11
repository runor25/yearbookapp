from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    year_of_graduation = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    about_me = models.TextField(blank=True)
    can_post = models.BooleanField(default=False)
    linkedin = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    instagram = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
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


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# def create_user(email, password):
#     user = User.objects.create_user(username=email, email=email, password=password)
#     user.save()
#     return user

# def create_student_profile(user, data):
#     student = Student.objects.create(
#         user=user,
#         first_name=data['first_name'],
#         last_name=data['last_name'],
#         # ... other fields ...
#     )
#     return student
