from django.contrib import admin
from .models import  LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification, JobTitle

admin.site.register(LanguageList)
admin.site.register(SpeakingProficiencyList)
admin.site.register(ReadingProficiencyList)
admin.site.register(WritingProficiencyList)
admin.site.register(ComputerSkillsList)
admin.site.register(ComputerProficiency)
admin.site.register(SoftSkillsList)
admin.site.register(SoftProficiency)
admin.site.register(Institution)
admin.site.register(Qualification)
admin.site.register(JobTitle)

