# Generated by Django 5.0.7 on 2024-09-11 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_eventimage_event_eventimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
