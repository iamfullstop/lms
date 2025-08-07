from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),

    # Dashboard views
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    # path('profile/', views.profile, name='profile'),

] 