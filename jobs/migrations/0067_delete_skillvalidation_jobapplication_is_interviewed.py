# Generated by Django 4.2.15 on 2025-02-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0066_delete_skillvalidation_interviewer_score'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='jobapplication',
            name='is_interviewed',
            field=models.BooleanField(default=False),
        ),
    ]
