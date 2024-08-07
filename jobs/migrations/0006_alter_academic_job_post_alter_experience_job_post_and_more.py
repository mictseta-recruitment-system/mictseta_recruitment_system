# Generated by Django 4.2.11 on 2024-06-15 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_jobpost_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='jobs.jobpost'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='jobs.jobpost'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='jobs.jobpost'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='job_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='jobs.jobpost'),
        ),
    ]
