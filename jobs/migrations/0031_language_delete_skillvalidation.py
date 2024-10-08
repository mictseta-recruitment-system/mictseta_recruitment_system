# Generated by Django 4.2.15 on 2024-09-22 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_industry'),
        ('jobs', '0030_delete_skillvalidation_jobapplication_filterd_out'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='j_languages', to='jobs.jobpost')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='j_language', to='config.languagelist')),
                ('reading_proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='j_reading', to='config.readingproficiencylist')),
                ('speaking_proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='j_speaking', to='config.speakingproficiencylist')),
                ('writing_proficiency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='j_writing', to='config.writingproficiencylist')),
            ],
        ),
        
    ]
