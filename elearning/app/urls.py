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

    path("student/enrolled-courses/", views.enrolled_courses, name="enrolled_courses"),

    # Course CRUD
    path('course/create/', views.course_create , name='create_courses'),
    path('course/list/', views.course_list, name='list_courses'),
    path('course/detail/<int:course_id>/', views.course_detail, name="detail_courses"),
    path('course/edit/<int:course_id>/', views.course_edit, name="edit_courses"),
    path('course/delete/<int:course_id>', views.course_delete, name="delete_courses"),
    path('viewcourse/<int:course_id>/', views.view_course, name="view_course"),


    path("course/<int:course_id>/content/", views.course_content, name="course_content"),

    # Section CRUD [course --> section]
    path('sections/create/<int:course_id>/', views.section_create, name='create_section'),
    path('sections/delete/<int:section_id>/', views.section_delete, name='delete_section'),
    # path('sections/list/<int:course_id>/', views.section_list, name='list_section'),
    # path('sections/update/<int:section_id>/', views.update_section, name='update_section'),

    # Lectures (nested under section)
    path('lectures/create/<int:section_id>/', views.lecture_create, name='create_lecture'),
    path('lectures/delete/<int:lecture_id>/', views.lecture_delete, name='delete_lecture'),
  
    

    # Payment
    path('course/<int:course_id>/payment/', views.process_payment, name="process_payment"),
    path('course/<int:course_id>/payment/success/', views.payment_success, name='payment_success'),
    path('course/<int:course_id>/payment/failure/', views.payment_failure, name='payment_failure'),

    # Review
    path("course/<int:course_id>/reviews/",   views.review_list, name="review_list"),
    path("course/<int:course_id>/reviews/create/",   views.review_create, name="review_create"),
    path("reviews/<int:review_id>/update/",   views.review_update, name="review_update"),
    path("reviews/<int:review_id>/delete/",   views.review_delete, name="review_delete"),

    # Certificate
    path("course/<int:course_id>/certificate/", views.view_certificate, name="view_certificate")

]





