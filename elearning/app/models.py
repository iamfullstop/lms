from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, 
    choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return f"{self.email} - {self.role}"


class Course(models.Model):
    LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    CATEGORIES = [
        ('development', 'Development'),
        ('business', 'Business'),
        ('finance_accounting', 'Finance & Accounting'),
        ('it_software', 'IT & Software'),
        ('office_productivity', 'Office Productivity'),
        ('personal_development', 'Personal Development'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
        ('lifestyle', 'Lifestyle'),
        ('photography_video', 'Photography & Video'),
        ('health_fitness', 'Health & Fitness'),
        ('music', 'Music'),
        ('teaching_academics', 'Teaching & Academics'),
    ]

    title = models.CharField(null=False, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instructor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='courses',
        limit_choices_to={'role': 'instructor'}
    )
    category = models.CharField(max_length=50, choices=CATEGORIES, default='development')
    level = models.CharField(max_length=20, choices=LEVELS, default='beginner')
    thumbnail_img = models.ImageField(upload_to='thumbnail/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    offer_certificate = models.BooleanField(default=False)
    description = models.TextField(null=False)
    requirements = models.TextField(null=False)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return f"{self.title} - {self.instructor} - {self.price}"


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - Section {self.order}: {self.title}"

class Lecture(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_previewable = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    video = models.FileField( upload_to='lecture_videos/', blank=True, null=True, help_text="Upload video file ")
    resource_file = models.FileField( upload_to='lecture_files/', blank=True, null=True, help_text="Upload resource file (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Section {self.section.order} • Lecture {self.order}: {self.title}"
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # avoid duplicate enrollments

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=1)  # 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course", "user")  # one review per course per student
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.course.title} ({self.rating}★)"

    @staticmethod
    def course_rating_summary(course_id):
        from django.db.models import Avg, Count
        return Review.objects.filter(course_id=course_id).aggregate(
            avg_rating=Avg("rating"),
            total_reviews=Count("id")
        )


class Certificate(models.Model):
    # Link to the enrollment (one-to-one: one enrollment → one certificate)
    enrollment = models.OneToOneField(
        "Enrollment", 
        on_delete=models.CASCADE, 
        related_name="certificate"
    )

    # Unique certificate identifier
    certificate_id = models.CharField(
        max_length=50, 
        unique=True, 
        default=uuid.uuid4, 
        editable=False
    )

    # When it was issued
    issued_at = models.DateTimeField(auto_now_add=True)

    # Optional: allow re-download (PDF path or saved file)
    pdf_file = models.FileField(
        upload_to="certificates/", 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"Certificate {self.certificate_id} for {self.enrollment.user}"

    class Meta:
        ordering = ["-issued_at"]
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
