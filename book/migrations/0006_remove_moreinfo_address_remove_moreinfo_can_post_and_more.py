# Generated by Django 5.0.7 on 2024-09-27 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_moreinfo_remove_student_about_me_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moreinfo',
            name='address',
        ),
        migrations.RemoveField(
            model_name='moreinfo',
            name='can_post',
        ),
        migrations.RemoveField(
            model_name='moreinfo',
            name='department',
        ),
        migrations.RemoveField(
            model_name='moreinfo',
            name='year_of_graduation',
        ),
        migrations.AddField(
            model_name='student',
            name='can_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_admission',
            field=models.IntegerField(choices=[(2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)], default=2017),
        ),
    ]