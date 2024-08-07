# Generated by Django 4.2.11 on 2024-06-12 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('location', models.CharField(max_length=225)),
                ('salary_range', models.CharField(max_length=100, null=True)),
                ('job_type', models.CharField(default='Full-time', max_length=50)),
                ('industry', models.CharField(max_length=100, null=True)),
                ('company_name', models.CharField(max_length=225, null=True)),
                ('application_deadline', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=50)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobpost')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.BooleanField(default=False)),
                ('proof_of_residence', models.BooleanField(default=False)),
                ('id_copy', models.BooleanField(default=False)),
                ('other_documents', models.BooleanField(null=True)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobpost')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('duration', models.CharField(max_length=10)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobpost')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=225)),
                ('qualification', models.CharField(max_length=225)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobpost')),
            ],
        ),
    ]
