# Generated by Django 4.2.15 on 2025-02-18 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0067_delete_skillvalidation_jobapplication_is_interviewed'),
    ]

    operations = [
      
        migrations.AddField(
            model_name='jobpost',
            name='is_interviewed',
            field=models.BooleanField(default=False),
        ),
    ]
