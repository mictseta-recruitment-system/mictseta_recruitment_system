# Generated by Django 4.2.15 on 2024-10-30 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0040_delete_skillvalidation_alter_jobapplication_reason'),
    ]

    operations = [
     
        migrations.AddField(
            model_name='jobpost',
            name='is_filter',
            field=models.BooleanField(default=False),
        ),
    ]