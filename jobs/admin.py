from django.contrib import admin
from .models import Language, JobPost, Academic, ComputerSkill, SoftSkill, Experience, Requirement, JobApplication, Interview, FeedBack, Quiz,QuizResults,Alert
# Register your models here.

admin.site.register(Academic)
admin.site.register(ComputerSkill)
admin.site.register(SoftSkill)
admin.site.register(Experience)
admin.site.register(Requirement)
admin.site.register(JobApplication)
admin.site.register(Interview)
admin.site.register(FeedBack)
admin.site.register(JobPost)
admin.site.register(Language)
admin.site.register(QuizResults)
admin.site.register(Quiz)
admin.site.register(Alert)


