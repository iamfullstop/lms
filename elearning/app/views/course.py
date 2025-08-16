from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Course, Section, Enrollment
import hmac, hashlib, base64, json
from django.utils import timezone


def published_courses(request):
    published_courses = Course.objects.filter(is_published=True).order_by("-created_at")
    context = {"courses": published_courses}
    return render(request, "course/published_courses.html", context)


def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_published=True)
    sections = Section.objects.filter(course=course).prefetch_related("lectures")

    # calculate total lectures
    total_lectures = sum(section.lectures.count() for section in sections)

    # Check if user purchased/enrolled
    purchased = False
    if request.user.is_authenticated:
        purchased = Enrollment.objects.filter(user=request.user, course=course).exists()

    return render(
        request,
        "course/viewcourse.html",
        {
            "course": course,
            "sections": sections,
            "total_lectures": total_lectures,
            "purchased": purchased,
        },
    )



@login_required
def process_payment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    now = timezone.now()

    SECRET_KEY = b"8gBm/:&EnhH.1/q"  # UAT SecretKey

    # Payment parameters
    total_amount = str(course.price)
    transaction_uuid = f"{course.id}-{user.id}-{int(now.timestamp())}"
    product_code = "EPAYTEST"
    signed_field_names = "total_amount,transaction_uuid,product_code"

    # Signature creation (HMAC-SHA256 + base64)
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    signature = hmac.new(SECRET_KEY, message.encode("utf-8"), hashlib.sha256)
    esewa_signature = base64.b64encode(signature.digest()).decode("utf-8")

    # Correct absolute URLs without double slashes
    base_url = request.build_absolute_uri('/')[:-1]  # removes trailing slash
    success_url = f"{base_url}/course/{course.id}/payment/success/"
    failure_url = f"{base_url}/course/{course.id}/payment/failure/"

    context = {
        "course": course,
        "user": user,
        "transaction_uuid": transaction_uuid,
        "success_url": success_url,
        "failure_url": failure_url,
        "esewa_signature": esewa_signature,
    }

    return render(request, "payment/payment.html", context)


@login_required
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    data = request.GET.get('data', None)
    esewa_data = {}
    if data:
        try:
            decoded = base64.b64decode(data).decode('utf-8')
            esewa_data = json.loads(decoded)
        except Exception as e:
            esewa_data = {"error": str(e)}

    # Enroll the user if payment successful
    Enrollment.objects.get_or_create(user=request.user, course=course)

    return render(request, 'payment/success.html', {
        'course': course,
        'esewa_data': esewa_data
    })

@login_required
def payment_failure(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'payment/failure.html', {'course': course})


@login_required
def course_create(request):
    if not hasattr(request.user, "role") or request.user.role != "instructor":
        messages.error(request, "You do not have permission to create a course.")
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        category = request.POST.get("category")  # updated field name
        level = request.POST.get("level")
        description = request.POST.get("description")
        requirements = request.POST.get("requirements")
        is_published = request.POST.get("is_published") == "on"
        offer_certificate = request.POST.get("offer_certificate") == "on"
        thumbnail_img = request.FILES.get("thumbnail_img")

        if (
            not title
            or not price
            or not category
            or not description
            or not requirements
        ):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "course/course_create.html")

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
                instructor=request.user,
            )
            messages.success(request, f"Course '{course.title}' created successfully!")
            return redirect("create_section", course_id=course.pk)
        except Exception as e:
            messages.error(request, f"Error creating course: {e}")

    return render(request, "course/course_create.html")


@login_required
def course_list(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, "course/course_list.html", {"courses": courses})


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    sections = course.sections.all()
    return render(
        request, "course/course_detail.html", {"course": course, "sections": sections}
    )


@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if (
        not hasattr(request.user, "role")
        or request.user.role != "instructor"
        or course.instructor != request.user
    ):
        messages.error(request, "You do not have permission to edit this course.")
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        category = request.POST.get("category")  # updated field name
        level = request.POST.get("level")
        description = request.POST.get("description")
        requirements = request.POST.get("requirements")
        is_published = request.POST.get("is_published") == "on"
        offer_certificate = request.POST.get("offer_certificate") == "on"
        thumbnail_img = request.FILES.get("thumbnail_img")

        if (
            not title
            or not price
            or not category
            or not description
            or not requirements
        ):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "course/course_edit.html", {"course": course})

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
            return redirect("detail_courses", course_id=course.pk)
        except Exception as e:
            messages.error(request, f"Error updating course: {e}")

    return render(request, "course/course_edit.html", {"course": course})


@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if (
        not hasattr(request.user, "role")
        or request.user.role != "instructor"
        or course.instructor != request.user
    ):
        messages.error(request, "You do not have permission to delete this course.")
        return redirect("/")

    if request.method == "POST":
        course.delete()
        messages.success(
            request, f"Course '{course.title}' has been deleted successfully."
        )
        return redirect("list_courses")

    return render(request, "course/course_delete.html", {"course": course})


@login_required
def course_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sections = course.sections.prefetch_related("lectures").all()
    return render(
        request, "course/course_content.html", {"course": course, "sections": sections}
    )
