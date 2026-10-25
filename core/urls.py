from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("skill-assessment/", views.skill_assessment, name="skill_assessment"),
    path("skill-gap/", views.skill_gap, name="skill_gap"),
    path("career-recommendation/", views.career_recommendation, name="career_recommendation"),
    path("learning-recommendation/", views.learning_recommendation, name="learning_recommendation"),
]