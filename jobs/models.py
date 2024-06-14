from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=False, null=False)
    description = models.TextField(null=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=False)
    location = models.CharField(max_length=225, unique=False, null=False)
    salary_range = models.CharField(max_length=100, null=True)  # Added field for salary range
    job_type = models.CharField(max_length=50, null=False, default='Full-time')  # Added field for job type
    industry = models.CharField(max_length=100, null=True)  # Added field for industry
    company_name = models.CharField(max_length=225, null=True)  # Added field for company name
    def __str__(self):
        return f'{self.title} Job Post'


class Academic(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    level = models.CharField(max_length=225, unique=False, null=False)
    qualification = models.CharField(max_length=225, unique=False, null=False)

    def __str__(self):
        return f'{self.level} Academic for {self.job_post.title} Job Post'


class Skill(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, unique=False, null=False)
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, null=False)

    def __str__(self):
         return f'{self.name} Skill for {self.job_post.title} Job Post'


class Experience(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, unique=False, null=False)
    duration = models.CharField(max_length=10, unique=False, null=False)

    def __str__(self):
        return f'{self.name} Experience for {self.job_post.title} Job Post'

class Requirement(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    description = models.CharField(max_length=10, unique=False, null=False)

    def __str__(self):
        return f'Requirements for {self.job_post.title} Job Post'

# class Requirement(models.Model):
#     job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
#     cv = models.BooleanField(default=False, null=False)
#     proof_of_residence = models.BooleanField(default=False, null=False)
#     id_copy = models.BooleanField(default=False, null=False)
#     other_documents = models.BooleanField(null=True)  # Added field for other documents

#     def __str__(self):
#         return f'Requirements for {self.job_post.title} Job Post'
