# Generated by Django 4.2.15 on 2024-09-11 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0027_profile_verification_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='verification_token',
        ),
    ]
