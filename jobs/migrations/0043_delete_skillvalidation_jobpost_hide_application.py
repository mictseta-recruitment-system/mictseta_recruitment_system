# Generated by Django 4.2.15 on 2024-10-31 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0042_delete_skillvalidation_jobapplication_hide'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='jobpost',
            name='hide_application',
            field=models.BooleanField(default=False),
        ),
    ]