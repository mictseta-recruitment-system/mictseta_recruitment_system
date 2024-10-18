from rest_framework import serializers
from jobs.models import JobPost, JobApplication,Academic, Skill, Experience, Requirement
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model 
from rest_framework import serializers
from profiles.models import Profile, Qualification, Language, ComputerSkills, SoftSkills, WorkingExpereince, AddressInformation, ProfileImage, SupportingDocuments
User = get_user_model()

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['highest_qualification', 'field_of_study', 'institution', 'year_obtained', 'status', 'grade']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['language', 'reading_proficiency', 'writing_proficiency', 'speaking_proficiency']

class ComputerSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerSkills
        fields = ['skill', 'level']

class SoftSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkills
        fields = ['skill', 'level']

class WorkingExpereinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingExpereince
        fields = ['job_title', 'company', 'location', 'start_date', 'end_date', 'years_of_experience']

class AddressInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInformation
        fields = ['street_address_line', 'street_address_line1', 'city', 'province', 'postal_code']

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['image', 'uploaded_at']

class SupportingDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportingDocuments
        fields = ['document', 'document_type', 'uploaded_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
 
class ProfileSerializer(serializers.ModelSerializer):
    qualifications = QualificationSerializer(many=True, )
    languages = LanguageSerializer(many=True,  )
    computer_skills = ComputerSkillsSerializer(many=True, )
    soft_skills = SoftSkillsSerializer(many=True, )
    working_experience = WorkingExpereinceSerializer(many=True, )
    address_information = AddressInformationSerializer()
    profile_image = ProfileImageSerializer( )
    supporting_documents = SupportingDocumentsSerializer(many=True, ) 
    class Meta:
        model = Profile
        fields = [
            'id','user', 'idnumber', 'phone', 'dob', 'gender', 'age', 'maritial_status', 
            'race', 'disability', 'is_verified', 'linkedin_profile', 'personal_website', 
            'uuid','name','surname', 'qualifications', 'languages', 'computer_skills', 'soft_skills', 
            'working_experience', 'address_information', 'profile_image', 'supporting_documents'
        ]
class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic
        fields = ['level', 'qualification']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name', 'level']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['name', 'duration']

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['description']

class JobPostSerializer(serializers.ModelSerializer):
    educations = AcademicSerializer(many=True)
    skills = SkillSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    requirements = RequirementSerializer(many=True)

    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'location', 
            'salary_range', 'job_type', 'industry', 'company_name', 'status',
            'is_complete', 'is_approved', 'educations', 'skills', 'experiences', 'requirements'
        ]

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'    

