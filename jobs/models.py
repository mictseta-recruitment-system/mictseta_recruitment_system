from django.db import models
from django.contrib.auth.models import User
from config.models import JobTitle, Industry
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.ForeignKey(JobTitle, on_delete=models.CASCADE, default=1)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, default=1)
    description = models.TextField(null=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=False)
    location = models.CharField(max_length=225, unique=False, null=False)
    salary_range = models.CharField(max_length=100, null=True) 
    job_type = models.CharField(max_length=50, null=False, default='Full-time') 
    status = models.CharField(max_length=20, null=False, default="waiting")
    is_complete = models.BooleanField(null=False, default=False)
    is_approved = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True)
    is_filter= models.BooleanField(null=False, default=False)
    hide_application = models.BooleanField(null=False,default=False)
    current_step = models.IntegerField(null=False, default=1)
    req_finance_approval = models.BooleanField(null=False, default=False)
    req_ceo_approval = models.BooleanField(null=False, default=False)
    def __str__(self):
        return f'{self.title} '

class Alert(models.Model):
    vacancy = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="alert3")
    note = models.CharField(max_length=250, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=False, default=False)
    status = models.CharField(max_length=250, null=False,default="pending")
    step = models.IntegerField(null=False)

 
class Academic(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='educations')
    field_of_study = models.ForeignKey(Qualification, on_delete=models.CASCADE) 
    nqf_level = models.ForeignKey(NQF, on_delete=models.CASCADE) 
    def __str__(self):
        return f'{self.field_of_study} {self.nqf_level}'

class ComputerSkill(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,  related_name='C_skills')
    name =  models.ForeignKey(ComputerSkillsList, on_delete=models.CASCADE)
    level = models.ForeignKey(ComputerProficiency, on_delete=models.CASCADE)
    is_required = models.BooleanField(null=False, default=False)
    def __str__(self):
         return f'{self.name} {self.level}'

class SoftSkill(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE,  related_name='S_skills')
    name =  models.ForeignKey(SoftSkillsList, on_delete=models.CASCADE)
    level = models.ForeignKey(SoftProficiency, on_delete=models.CASCADE)
    is_required = models.BooleanField(null=False, default=False)
    def __str__(self):
         return f'{self.name} {self.level}'

class Experience(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='experiences')
    name = models.CharField(max_length=225, unique=False, null=False)
    duration = models.CharField(max_length=40, unique=False, null=False)
    def __str__(self):
        return f'{self.name} {self.duration}'

class Requirement(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='requirements')
    description = models.CharField(max_length=225, unique=False, null=False)
    def __str__(self):
        return f'{self.description} {self.job_post}'

class Language(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='j_languages')
    language = models.ForeignKey(LanguageList, on_delete=models.CASCADE, related_name='j_language')
    reading_proficiency = models.ForeignKey(ReadingProficiencyList, on_delete=models.CASCADE, related_name='j_reading')
    writing_proficiency = models.ForeignKey(WritingProficiencyList, on_delete=models.CASCADE, related_name='j_writing')
    speaking_proficiency = models.ForeignKey(SpeakingProficiencyList, on_delete=models.CASCADE, related_name='j_speaking')
    def __str__(self):
        return f" {self.language}"

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
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="s_applications", null=True)    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    previous_stage = models.CharField(max_length=100, null=True)
    current_stage = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=False)
    
    hide = models.BooleanField(null=False, default=False)
    is_filter = models.BooleanField(null=False, default=False)
    filterd_out = models.BooleanField(null=False, default=False)
    is_rejected = models.BooleanField(null=False, default=False)
    reason = models.CharField(null=True, max_length=100, default="")
    is_filter_applied = models.BooleanField(null=False, default=False)


    def __str__(self):
        return f'{self.user.email} - {self.job.title}'

class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applicant")
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name="application")
    date = models.CharField(max_length=225,null=False)
    start_time = models.CharField(max_length=225,null=False)
    end_time = models.CharField(max_length=225,null=False)
    def __str__(self):
        return f'{self.application}'

class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=225,null=False)
    status = models.CharField(max_length=225,null=False)
    def __str__(self):
        return f'{self.user.email} - {self.job.title}'



class Quiz(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE,related_name="quiz")
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

class QuizResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.CharField(max_length=100)
    results =  models.CharField(max_length=225,null=False)

class QuizAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


    def __str__(self):
        return self.quiz.title