# Generated by Django 4.2.15 on 2024-09-15 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0031_profile_address_information_profile_computer_skills_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='surname',
            field=models.CharField(default='', max_length=150, null=True),
        ),
    ]
