from django.contrib import admin
from .models import StudentProfile, SkillAssessment, LearningResource


admin.site.register(StudentProfile)
admin.site.register(SkillAssessment)
admin.site.register(LearningResource)