from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import StudentProfile, SkillAssessment


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")

        else:
            return render(
                request,
                "core/login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "core/login.html")


def register_view(request):
 
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "core/register.html",
                {"error": "Username already exists"}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "core/register.html") 



def dashboard(request):

   
    assessment = SkillAssessment.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    # Default values
    skill_score = 0
    career_match = 0
    skills_to_improve = 0

    if assessment:

        
        skill_score = round(
            (
                assessment.programming +
                assessment.web_development +
                assessment.database +
                assessment.python +
                assessment.ai_ml
            ) / 5
        )

        
        career_match = skill_score

      
        skills = [
            assessment.programming,
            assessment.web_development,
            assessment.database,
            assessment.python,
            assessment.ai_ml
        ]

      
        skills_to_improve = sum(
            1 for skill in skills if skill < 50
        )

    return render(
        request,
        "core/dashboard.html",
        {
            "assessment": assessment,
            "skill_score": skill_score,
            "career_match": career_match,
            "skills_to_improve": skills_to_improve
        }
    )
    
def skill_gap(request):

    assessment = SkillAssessment.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    skill_gaps = []

    if assessment:

        skills = [
            (
                "Programming",
                assessment.programming,
                "Data Structures, Algorithms, OOP, Problem Solving"
            ),
            (
                "Web Development",
                assessment.web_development,
                "HTML, CSS, JavaScript, React, Django"
            ),
            (
                "Database",
                assessment.database,
                "SQL, Joins, Normalization, Database Design"
            ),
            (
                "Python",
                assessment.python,
                "Python Fundamentals, OOP, NumPy, Pandas"
            ),
            (
                "AI / Machine Learning",
                assessment.ai_ml,
                "Machine Learning Algorithms, Scikit-learn, Model Evaluation"
            ),
        ]

        target_score = 70

        for skill_name, score, improvement in skills:

            if score < target_score:

                skill_gaps.append({
                    "name": skill_name,
                    "score": score,
                    "gap": target_score - score,
                    "improvement": improvement
                })

    return render(
        request,
        "core/skill_gap.html",
        {
            "assessment": assessment,
            "skill_gaps": skill_gaps
        }
    )
    


            

def logout_view(request):
    logout(request)
    return redirect("login")

def profile(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        college = request.POST.get("college")
        course = request.POST.get("course")
        year = request.POST.get("year")
        skills = request.POST.get("skills")
        career_goal = request.POST.get("career_goal")

        StudentProfile.objects.update_or_create(
            user=request.user,
            defaults={
                "full_name": full_name,
                "college": college,
                "course": course,
                "year": year,
                "skills": skills,
                "career_goal": career_goal,
            }
        )

        return render(
            request,
            "core/profile.html",
            {"message": "Profile saved successfully! ✅"}
        )

    return render(request, "core/profile.html")


def skill_assessment(request):

    if request.method == "POST":

        programming = int(request.POST.get("programming", 0))
        web_development = int(request.POST.get("web_development", 0))
        database = int(request.POST.get("database", 0))
        python = int(request.POST.get("python", 0))
        ai_ml = int(request.POST.get("ai_ml", 0))

        SkillAssessment.objects.create(
            user=request.user,
            programming=programming,
            web_development=web_development,
            database=database,
            python=python,
            ai_ml=ai_ml
        )

        return redirect("dashboard")

    return render(request, "core/skill_assessment.html")

def career_recommendation(request):

    assessment = SkillAssessment.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    recommendations = []

    if assessment:

        # Software Developer
        software_score = round(
            (
                assessment.programming +
                assessment.web_development +
                assessment.database
            ) / 3
        )

        # Python / AI Developer
        ai_score = round(
            (
                assessment.python +
                assessment.ai_ml +
                assessment.programming
            ) / 3
        )

        # Web Developer
        web_score = round(
            (
                assessment.web_development +
                assessment.programming
            ) / 2
        )

        recommendations = [
            {
                "career": "Software Developer",
                "score": software_score,
                "description": "Suitable for students interested in programming, software development and database technologies."
            },
            {
                "career": "AI / ML Developer",
                "score": ai_score,
                "description": "Suitable for students interested in Python, Artificial Intelligence and Machine Learning."
            },
            {
                "career": "Web Developer",
                "score": web_score,
                "description": "Suitable for students interested in frontend, backend and web application development."
            }
        ]

        # Sort careers according to matching score
        recommendations = sorted(
            recommendations,
            key=lambda x: x["score"],
            reverse=True
        )

    return render(
        request,
        "core/career_recommendation.html",
        {
            "assessment": assessment,
            "recommendations": recommendations
        }
    )
    
def learning_recommendation(request):

    assessment = SkillAssessment.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    learning_recommendations = []

    if assessment:

        skills = [
            ("Programming", assessment.programming,
             "Learn C/C++ programming, data structures and algorithms."),

            ("Web Development", assessment.web_development,
             "Learn HTML, CSS, JavaScript, Django and React."),

            ("Database", assessment.database,
             "Learn SQL, MySQL and database management concepts."),

            ("Python", assessment.python,
             "Learn Python fundamentals, OOP, libraries and problem solving."),

            ("AI / Machine Learning", assessment.ai_ml,
             "Learn Machine Learning, NumPy, Pandas, Scikit-learn and AI concepts.")
        ]

        target_score = 70

        for skill_name, score, recommendation in skills:

            if score < target_score:

                learning_recommendations.append({
                    "skill": skill_name,
                    "score": score,
                    "gap": target_score - score,
                    "recommendation": recommendation
                })

    return render(
        request,
        "core/learning_recommendation.html",
        {
            "assessment": assessment,
            "learning_recommendations": learning_recommendations
        }
    )

