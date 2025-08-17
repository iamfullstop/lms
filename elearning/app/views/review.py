from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from app.models import Course, Review, Enrollment

def review_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = course.reviews.select_related("user").values(
        "id", "user__full_name", "rating", "comment", "created_at"
    )
    summary = Review.course_rating_summary(course.id)
    return JsonResponse({
        "reviews": list(reviews),
        "avg_rating": round(summary["avg_rating"] or 0, 1),
        "total_reviews": summary["total_reviews"],
    })


@login_required
@require_POST
def review_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return JsonResponse({"error": "You must be enrolled to review."}, status=403)

    rating = int(request.POST.get("rating", 0))
    comment = request.POST.get("comment", "")

    review, created = Review.objects.update_or_create(
        course=course, user=request.user,
        defaults={"rating": rating, "comment": comment},
    )

    return JsonResponse({"success": True, "review_id": review.id})


@login_required
@require_POST
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.rating = int(request.POST.get("rating", review.rating))
    review.comment = request.POST.get("comment", review.comment)
    review.save()
    return JsonResponse({"success": True})


@login_required
@require_POST
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return JsonResponse({"success": True})
