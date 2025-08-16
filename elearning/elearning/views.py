from django.shortcuts import render
from app.models import Course

def index(request):
    # Get latest 3 published courses
    recent_courses = Course.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'index.html', {'recent_courses': recent_courses})
