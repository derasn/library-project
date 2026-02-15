from django.shortcuts import render, get_object_or_404, redirect
from .models import Subject, Course, Material
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
import hashlib

# Create your views here.


def get_file_hash(uploaded_file):
    hasher = hashlib.sha256()

    for chunk in uploaded_file.chunks():
        hasher.update(chunk)

    uploaded_file.seek(0)

    return hasher.hexdigest()


def home(request):
    subject = Subject.objects.all()
    course = Course.objects.all()
    levels = [100, 200, 300, 400]
    recent_materials = Material.objects.all().order_by('-uploaded_at')[:4]

    context = {
        'subject' : subject,
        'courses' : course,
        'levels' : levels,
        'materials' : recent_materials,
    }
    return render(request,'home.html', context)


def subject_courses(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    courses = subject.courses.all()
    context = {
        'subject' : subject,
        'courses' : courses,
    }
    return render(request, 'subject_courses.html', context)


def level_courses(request, level):
    courses = Course.objects.filter(level=level)
    context =  {
        'courses' : courses,
        'level' : level,
    }
    return render(request, 'level_courses.html', context)


def course_details(request, course_id):
    courses = Course.objects.get(id=course_id)
    materials = courses.materials.all()
    context = {
        'course' : courses,
        'materials' : materials,
    }
    return render(request, 'course_details.html', context)


def search(request):
    query = request.GET.get("q", "").strip()

    materials = Material.objects.all()

    if query:
        results = materials.filter(
            Q(course_code__subject__name__icontains=query) |
            Q(course_code__course_code__icontains=query) |
            Q(course_code__title__icontains=query) |
            Q(description__icontains=query) |
            Q(year_used__icontains=query) |
            Q(file__icontains=query)
        )

    context = {
        'query' : query,
        'results' : results,
    }

    return render(request, 'search_results.html', context)



def upload_material(request):
    courses = Course.objects.all()
    errors = []

    if request.method == 'POST':
        course_id = request.POST.get('course_code')
        course_code = get_object_or_404(Course, pk=course_id)

        material_description = request.POST.get('description', '')
        year_used = request.POST.get('year_used', '')
        uploaded_material = request.FILES.get('file')

        if uploaded_material:
            file_hash = get_file_hash(uploaded_material)

            if Material.objects.filter(file_hash=file_hash):
                errors.append("Hi, this material has already been uploaded. Thanks for the effort.")

            else:
                new_upload = Material(
                    course_code = course_code,
                    description = material_description,
                    year_used = year_used,
                    file = uploaded_material,
                    file_hash = file_hash,
                )

                try:
                    new_upload.full_clean()
                    new_upload.save()
                    messages.success(request, "Material uploaded successfully!")
                    return redirect('home')
                
                except ValidationError as err:
                    errors = err.messages

        else:
            errors.append("Please select a file to upload.")

    return render(request, 'upload.html', {'courses': courses, 'errors': errors})



def register_course(request):
    subjects = Subject.objects.all()

    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        title = request.POST.get('title', '')

        subject_id = request.POST.get('subject')
        subject = get_object_or_404(Subject, pk=subject_id)

        level = request.POST.get('level')

        if course_code:
            new_course = Course(
                course_code = course_code,
                title = title,
                subject = subject,
                level = level
            )
            new_course.save()
            messages.success(request, "Course added successfully!")
            return redirect('home')
        
    return render(request, 'register.html', {'subjects': subjects})