from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Student, Course, Enrollment, FileUpload
from .forms import StudentRegistrationForm, CourseEnrollmentForm, FileUploadForm, AdminRegistrationForm

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Teacher account created for {username}! You can now login and access the admin panel.')
            return redirect('login')
    else:
        form = AdminRegistrationForm()
    return render(request, 'registration/admin_register.html', {'form': form})

@login_required
def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by('title')
    user_enrollments = []
    
    if hasattr(request.user, 'student'):
        user_enrollments = Enrollment.objects.filter(
            student=request.user.student,
            is_active=True
        ).values_list('course_id', flat=True)
    
    return render(request, 'students/course_list.html', {
        'courses': courses,
        'user_enrollments': user_enrollments
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    files = []
    
    if hasattr(request.user, 'student'):
        is_enrolled = Enrollment.objects.filter(
            student=request.user.student,
            course=course,
            is_active=True
        ).exists()
        
        if is_enrolled:
            files = FileUpload.objects.filter(course=course).order_by('-timestamp')
    
    return render(request, 'students/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'files': files
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('course_list')
    
    student = request.user.student
    
    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST, student=student, course=course)
        if form.is_valid():
            enrollment = Enrollment.objects.create(student=student, course=course)
            messages.success(request, f'Successfully enrolled in {course.title}!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseEnrollmentForm(student=student, course=course)
    
    return render(request, 'students/enroll_course.html', {
        'form': form,
        'course': course
    })

@login_required
def my_courses(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Only students can view enrolled courses.')
        return redirect('course_list')
    
    enrollments = Enrollment.objects.filter(
        student=request.user.student,
        is_active=True
    ).select_related('course')
    
    return render(request, 'students/my_courses.html', {
        'enrollments': enrollments
    })

@login_required
def upload_file(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is enrolled in the course
    if hasattr(request.user, 'student'):
        if not Enrollment.objects.filter(
            student=request.user.student,
            course=course,
            is_active=True
        ).exists():
            messages.error(request, 'You must be enrolled in this course to upload files.')
            return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.uploaded_by = request.user
            file_upload.course = course
            file_upload.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = FileUploadForm()
    
    return render(request, 'students/file_upload.html', {
        'form': form,
        'course': course
    })

@login_required
def download_file(request, file_id):
    file_upload = get_object_or_404(FileUpload, id=file_id)
    
    # Check if user is enrolled in the course
    if hasattr(request.user, 'student'):
        if not Enrollment.objects.filter(
            student=request.user.student,
            course=file_upload.course,
            is_active=True
        ).exists() and not request.user.is_staff:
            raise PermissionDenied("You don't have permission to download this file.")
    
    try:
        response = HttpResponse(file_upload.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_upload.get_file_name()}"'
        return response
    except:
        raise Http404("File not found.")

@login_required
def delete_file(request, file_id):
    file_upload = get_object_or_404(FileUpload, id=file_id)
    
    # Check if user can delete the file (owner or admin)
    if file_upload.uploaded_by != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this file.")
        return redirect('course_detail', course_id=file_upload.course.id)
    
    if request.method == 'POST':
        course_id = file_upload.course.id
        file_upload.delete()
        messages.success(request, 'File deleted successfully!')
        return redirect('course_detail', course_id=course_id)
    
    return render(request, 'students/delete_file.html', {
        'file_upload': file_upload
    })
