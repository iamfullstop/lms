from django.contrib import admin
from .models import User,Course, Section, Lecture, Enrollment

# Register your models here.

admin.site.register(User)
admin.site.register(Course)  

admin.site.register(Section)
admin.site.register(Lecture)

admin.site.register(Enrollment)