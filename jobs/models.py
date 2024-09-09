from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=225, unique=False, null=False)
    description = models.TextField(null=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=False)
    location = models.CharField(max_length=225, unique=False, null=False)
    salary_range = models.CharField(max_length=100, null=True)  # Added field for salary range
    # LEVEL_CHOICES = [
    #     ('Remote', 'Remote'),
    #     ('Part-Time', 'Part-Time'),
    #     ('Full-Time', 'Full-Time'),
    # ]
    job_type = models.CharField(max_length=50, null=False, default='Full-time')  # Added field for job type
    industry = models.CharField(max_length=100, null=True)  # Added field for industry
    company_name = models.CharField(max_length=225, null=True)  # Added field for company name
    status = models.CharField(max_length=20, null=False, default="waiting")
    is_complete = models.BooleanField(null=False, default=False)
    is_approved = models.BooleanField(null=False, default=False)
    
   
    def __str__(self):
        return f'{self.title} Job Vacancy, owened by : {self.user.first_name} {self.user.last_name}'


from django.db import models

class Academic(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='educations')
    level = models.CharField(max_length=225) 
    field_of_study = models.CharField(max_length=225, null=True, blank=True) 
    institution = models.CharField(max_length=255) 
    status = models.CharField(max_length=50)  
    transcript = models.FileField(upload_to='transcripts/', null=True, blank=True) 

    def __str__(self):
        return f'Academic for {self.job_post.title} - {self.level} at {self.institution}'



class Experience(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='experiences')
    name = models.CharField(max_length=225, unique=False, null=False)
    job_type = models.CharField(max_length=255)
    duration = models.IntegerField()  # Weeks/Months/Year
    def __str__(self):
        return f'Experience for {self.job_post.title} Job Vacancy'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    action = models.CharField(max_length=225, unique=False, null=False)
    job_title = models.CharField(max_length=225, unique=False, null=False)
    status = models.CharField(max_length=225, unique=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(null=False, default=False)
    def __str__(self):
        return f'Notification for {self.job_title} Job Vacancy'
# class Requirement(models.Model):
#     job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
#     cv = models.BooleanField(default=False, null=False)
#     proof_of_residence = models.BooleanField(default=False, null=False)
#     id_copy = models.BooleanField(default=False, null=False)
#     other_documents = models.BooleanField(null=True)  # Added field for other documents

#     def __str__(self):
#         return f'Requirements for {self.job_post.title} Job Post'


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=False)


class SkillValidation(models.Model):
    skill = models.CharField(max_length=100, null=True)
    level = models.CharField(max_length=15, null=True)
    category = models.CharField(max_length=20,null=True)

class SkillList(models.Model):
    skill_name = models.CharField(max_length=255)
    skill_type = models.CharField(max_length=50)

class LanguageList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
class UserLanguage(models.Model):
    PROFICIENCY_CHOICES = [
        ('Fair', 'Fair'),
        ('Good', 'Good'),
        ('Very Good', 'Very Good'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageList, on_delete=models.CASCADE)
    reading_proficiency = models.CharField(max_length=10, choices=PROFICIENCY_CHOICES)
    writing_proficiency = models.CharField(max_length=10, choices=PROFICIENCY_CHOICES)
    speaking_proficiency = models.CharField(max_length=10, choices=PROFICIENCY_CHOICES)
    
    
class VacancyLanguage(models.Model):
    vacancy = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageList, on_delete=models.CASCADE)
    proficiency_required = models.CharField(max_length=10, choices=UserLanguage.PROFICIENCY_CHOICES)