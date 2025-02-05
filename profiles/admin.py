from django.contrib import admin
from .models import Profile, Language, SoftSkills, ComputerSkills, Education,StaffProfile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Language)
admin.site.register(SoftSkills)
admin.site.register(ComputerSkills)
admin.site.register(Education)
admin.site.register(StaffProfile)
