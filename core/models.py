from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    college = models.CharField(max_length=150)
    course = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    skills = models.TextField(blank=True)
    career_goal = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class SkillAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    programming = models.IntegerField(default=0)
    web_development = models.IntegerField(default=0)
    database = models.IntegerField(default=0)
    python = models.IntegerField(default=0)
    ai_ml = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " Skill Assessment"


class LearningResource(models.Model):
    skill = models.CharField(max_length=100)

    title = models.CharField(max_length=200)

    resource_type = models.CharField(max_length=50)

    description = models.TextField(blank=True)

    url = models.URLField()

    level = models.CharField(max_length=50, default="Beginner")

    def __str__(self):
        return self.skill + " - " + self.title