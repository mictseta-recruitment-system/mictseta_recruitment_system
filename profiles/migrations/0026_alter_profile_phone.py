# Generated by Django 4.2.15 on 2024-09-10 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0025_alter_profile_age_alter_profile_disability_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=' ', max_length=10, null=True),
        ),
    ]
