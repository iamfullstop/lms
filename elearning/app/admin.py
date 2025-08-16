from django.contrib import admin
from .models import User,Course, Section, Lecture

# Register your models here.

admin.site.register(User)
admin.site.register(Course)  # Register the Course model

admin.site.register(Section)
admin.site.register(Lecture)
