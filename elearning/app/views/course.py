from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Course, Section

def published_courses(request):
    published_courses = Course.objects.filter(is_published=True).order_by('-created_at')
    context = {
        'courses': published_courses
    }
    return render(request, 'course/published_courses.html', context)


def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    sections = Section.objects.filter(course=course).prefetch_related("lectures")

    # calculate total lectures
    total_lectures = sum(section.lectures.count() for section in sections)

    return render(request, "course/viewcourse.html", {
        "course": course,
        "sections": sections,
        "total_lectures": total_lectures
    })

@login_required
def process_payment(request, course_id):
    # dummy payment handler (you can integrate Razorpay/Stripe later)
    course = get_object_or_404(Course, id=course_id, is_published=True)
    return render(request, "payment.html", {"course": course})

@login_required
def course_create(request):
    if not hasattr(request.user, 'role') or request.user.role != 'instructor':
        messages.error(request, "You do not have permission to create a course.")
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')  # updated field name
        level = request.POST.get('level')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        is_published = request.POST.get('is_published') == 'on'
        offer_certificate = request.POST.get('offer_certificate') == 'on'
        thumbnail_img = request.FILES.get('thumbnail_img')

        if not title or not price or not category or not description or not requirements:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'course/course_create.html')

        try:
            course = Course.objects.create(
                title=title,
                price=price,
                category=category,
                level=level,
                description=description,
                requirements=requirements,
                is_published=is_published,
                offer_certificate=offer_certificate,
                thumbnail_img=thumbnail_img,
                instructor=request.user
            )
            messages.success(request, f"Course '{course.title}' created successfully!")
            return redirect('create_section', course_id=course.pk)
        except Exception as e:
            messages.error(request, f"Error creating course: {e}")

    return render(request, 'course/course_create.html')


@login_required
def course_list(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'course/course_list.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    sections = course.sections.all()
    return render(request, 'course/course_detail.html', {
        'course': course,
        'sections': sections
    })


@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if not hasattr(request.user, 'role') or request.user.role != 'instructor' or course.instructor != request.user:
        messages.error(request, "You do not have permission to edit this course.")
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        category = request.POST.get('category')  # updated field name
        level = request.POST.get('level')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        is_published = request.POST.get('is_published') == 'on'
        offer_certificate = request.POST.get('offer_certificate') == 'on'
        thumbnail_img = request.FILES.get('thumbnail_img')

        if not title or not price or not category or not description or not requirements:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'course/course_edit.html', {'course': course})

        try:
            course.title = title
            course.price = price
            course.category = category
            course.level = level
            course.description = description
            course.requirements = requirements
            course.is_published = is_published
            course.offer_certificate = offer_certificate

            if thumbnail_img:
                course.thumbnail_img = thumbnail_img

            course.save()

            messages.success(request, f"Course '{course.title}' updated successfully!")
            return redirect('detail_courses', course_id=course.pk)
        except Exception as e:
            messages.error(request, f"Error updating course: {e}")

    return render(request, 'course/course_edit.html', {'course': course})


@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if not hasattr(request.user, 'role') or request.user.role != 'instructor' or course.instructor != request.user:
        messages.error(request, "You do not have permission to delete this course.")
        return redirect('/')

    if request.method == 'POST':
        course.delete()
        messages.success(request, f"Course '{course.title}' has been deleted successfully.")
        return redirect('list_courses')

    return render(request, 'course/course_delete.html', {'course': course})


@login_required
def course_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sections = course.sections.prefetch_related("lectures").all()
    return render(request, "course/course_content.html", {
        "course": course,
        "sections": sections
    })
