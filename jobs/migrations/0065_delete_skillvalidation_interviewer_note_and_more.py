# Generated by Django 4.2.15 on 2025-02-18 17:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0064_delete_skillvalidation_and_more'),
    ]

    operations = [
      
        migrations.AddField(
            model_name='interviewer',
            name='note',
            field=models.CharField(max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='interviewer',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
