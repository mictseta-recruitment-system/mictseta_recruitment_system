# Generated by Django 4.2.15 on 2024-10-23 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0036_answer_question_quiz_quizresults_and_more'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='quiz',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]