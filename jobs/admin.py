from django.contrib import admin
from .models import Academic, ComputerSkill, SoftSkill, Experience, Requirement, JobApplication, Interview, FeedBack
# Register your models here.

admin.site.register(Academic)
admin.site.register(ComputerSkill)
admin.site.register(SoftSkill)
admin.site.register(Experience)
admin.site.register(Requirement)
admin.site.register(JobApplication)
admin.site.register(Interview)
admin.site.register(FeedBack)


