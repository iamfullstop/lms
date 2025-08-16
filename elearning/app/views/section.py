from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Course, Section, Lecture


@login_required
def section_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        title = request.POST.get("title")
        order = request.POST.get("order")

        if not title or not order:
            return JsonResponse({"success": False, "error": "Title and order are required."})

        section = Section.objects.create(course=course, title=title, order=order)
        return JsonResponse({
            "success": True,
            "section": {
                "id": section.id,
                "title": section.title,
                "order": section.order
            }
        })

    sections = course.sections.prefetch_related("lectures")
    return render(request, "section/section_create.html", {"course": course, "sections": sections})


@login_required
def lecture_create(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == "POST":
        title = request.POST.get("title")
        order = request.POST.get("order")
        description = request.POST.get("description", "")
        video = request.FILES.get("video")
        is_previewable = request.POST.get("is_previewable") == 'true'
        resource_file = request.FILES.get("resource_file")

        if not title or not order:
            return JsonResponse({"success": False, "error": "Title and order are required."})

        lecture = Lecture.objects.create(
            section=section,
            title=title,
            order=order,
            description=description,
            video=video,
            resource_file=resource_file,
            is_previewable=is_previewable
        )

        return JsonResponse({
            "success": True,
            "lecture": {
                "id": lecture.id,
                "title": lecture.title,
                "order": lecture.order,
                "preview": lecture.is_previewable,
                "video_url": lecture.video.url if lecture.video else "",
                "resource_file_url": lecture.resource_file.url if lecture.resource_file else ""
            }
        })

    return JsonResponse({"success": False, "error": "Invalid request method"})


@login_required
def section_delete(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    course_id = section.course.id
    section.delete()
    return JsonResponse({"success": True, "course_id": course_id})


@login_required
def lecture_delete(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    section_id = lecture.section.id
    lecture.delete()
    return JsonResponse({"success": True, "section_id": section_id})
