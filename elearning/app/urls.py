from django.urls import path
from app import views
urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),

    path('student/', views.student_dashboard, name='student_dashboard'),
    path('profile', views.profile, name="profile"),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    path('publish/', views.published_courses, name='published_courses'),


    # Course CRUD
    path('course/create/', views.course_create , name='create_courses'),
    path('course/list/', views.course_list, name='list_courses'),
    path('course/detail/<int:course_id>/', views.course_detail, name="detail_courses"),
    path('course/edit/<int:course_id>/', views.course_edit, name="edit_courses"),
    path('course/delete/<int:course_id>', views.course_delete, name="delete_courses"),


    path("course/<int:course_id>/content/", views.course_content, name="course_content"),

    # Section CRUD [course --> section]
    path('sections/create/<int:course_id>/', views.section_create, name='create_section'),
    # path('sections/list/<int:course_id>/', views.section_list, name='list_section'),
    # path('sections/update/<int:section_id>/', views.update_section, name='update_section'),
    path('sections/delete/<int:section_id>/', views.section_delete, name='delete_section'),

    # Lectures (nested under section)
    path('lectures/create/<int:section_id>/', views.lecture_create, name='create_lecture'),
    path('lectures/delete/<int:lecture_id>/', views.lecture_delete, name='delete_lecture'),
    # Lecture CRUD 
    # path('lecture/create/', views.slecture_create , name='create_lectures'),
    # path('lecture/list/', views.lecture_list, name='list_lectures'),
    # path('lecture/edit/<int:pk>', views.lecture_edit, name="edit_lectures"),
    # path ('lecture/delete/<int:pk>', views.lecture_delete, name="delete_lectures")

    # Enrollment CRUD 
    # path('enrollment/create/', views.enrollment_create , name='create_enrollments'),
    # path('enrollment/list/', views.enrollment_list, name='list_enrollments'),
    # path('enrollment/edit/<int:pk>', views.enrollment_edit, name="edit_enrollments"),
    # path ('enrollment/delete/<int:pk>', views.enrollment_delete, name="delete_enrollments")


]


