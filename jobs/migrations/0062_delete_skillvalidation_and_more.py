# Generated by Django 4.2.15 on 2025-02-18 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0061_interviewscoreboard_interviewscorequestion_and_more'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='interviewscorequestion',
            name='scoreboard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interview_questions', to='jobs.interviewscoreboard'),
        ),
        migrations.AlterField(
            model_name='interviewscoreresult',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.interviewscorequestion'),
        ),
        migrations.AlterField(
            model_name='interviewscoreresult',
            name='scoreboard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interview_results', to='jobs.interviewscoreboard'),
        ),
    ]
