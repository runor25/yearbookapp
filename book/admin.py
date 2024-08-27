from django.contrib import admin
from .models import Student, Event, EventImage, Comment,EventImages

admin.site.register(Student)
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(EventImages)
admin.site.register(Comment)
