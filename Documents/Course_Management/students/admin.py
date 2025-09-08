from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from .models import Student, Course, Enrollment, FileUpload

# Customize the admin site header and title
admin.site.site_header = "Course Management System Administration"
admin.site.site_title = "Course Management Admin"
admin.site.index_title = "Welcome to Course Management Administration"

# Inline admin for Student in User admin
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Information'
    fields = ('student_id', 'phone_number', 'date_of_birth')

# Enhanced User Admin with Student information - Teacher/Admin Access Control
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_student', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def is_student(self, obj):
        return hasattr(obj, 'student')
    is_student.boolean = True
    is_student.short_description = 'Is Student'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Teachers/Admins can only see students and other teachers, not superusers
        return qs.filter(is_superuser=False)
    
    def has_add_permission(self, request):
        # Teachers can add students but not other admins
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return request.user.is_staff
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            # Teachers cannot modify superuser status
            readonly_fields.extend(['is_superuser', 'user_permissions', 'groups'])
        return readonly_fields

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'student_id', 'get_email', 'phone_number', 'enrollment_count', 'created_at')
    list_filter = ('created_at', 'date_of_birth')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'student_id', 'phone_number')
    readonly_fields = ('created_at', 'enrollment_count', 'get_enrolled_courses')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Student Details', {
            'fields': ('student_id', 'phone_number', 'date_of_birth')
        }),
        ('Statistics', {
            'fields': ('enrollment_count', 'get_enrolled_courses', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Teachers/Admins can add students
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        # Teachers/Admins can edit student information
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete students
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        # Teachers/Admins can view student information
        return request.user.is_staff
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user.first_name else obj.user.username
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def enrollment_count(self, obj):
        count = obj.enrollment_set.filter(is_active=True).count()
        return format_html('<span style="color: {};">{}/5</span>', 
                          'red' if count >= 5 else 'green', count)
    enrollment_count.short_description = 'Enrollments'
    
    def get_enrolled_courses(self, obj):
        enrollments = obj.enrollment_set.filter(is_active=True).select_related('course')
        if enrollments:
            course_links = []
            for enrollment in enrollments:
                url = reverse('admin:students_course_change', args=[enrollment.course.pk])
                course_links.append(format_html('<a href="{}">{}</a>', url, enrollment.course.title))
            return mark_safe('<br>'.join(course_links))
        return "No enrollments"
    get_enrolled_courses.short_description = 'Enrolled Courses'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'credits', 'difficulty', 'enrollment_status', 'is_active', 'start_date', 'end_date')
    list_filter = ('difficulty', 'is_active', 'start_date', 'credits', 'instructor')
    search_fields = ('title', 'instructor', 'description')
    readonly_fields = ('created_at', 'enrollment_status', 'get_enrolled_students', 'get_file_count')
    list_editable = ('is_active',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'instructor')
        }),
        ('Course Settings', {
            'fields': ('credits', 'difficulty', 'max_students', 'is_active')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('enrollment_status', 'get_enrolled_students', 'get_file_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Teachers/Admins can add courses
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        # Teachers/Admins can edit courses
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        # Teachers/Admins can delete courses (but maybe restrict to course owners)
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        # Teachers/Admins can view courses
        return request.user.is_staff
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Teachers can see all courses, but could be restricted to their own courses
        return qs
    
    def enrollment_status(self, obj):
        enrolled = obj.get_enrolled_count()
        max_students = obj.max_students
        percentage = (enrolled / max_students) * 100 if max_students > 0 else 0
        
        if percentage >= 90:
            color = 'red'
        elif percentage >= 70:
            color = 'orange'
        else:
            color = 'green'
            
        return format_html(
            '<span style="color: {};">{}/{} ({}%)</span>',
            color, enrolled, max_students, int(percentage)
        )
    enrollment_status.short_description = 'Enrollment Status'
    
    def get_enrolled_students(self, obj):
        enrollments = obj.enrollment_set.filter(is_active=True).select_related('student__user')
        if enrollments:
            student_links = []
            for enrollment in enrollments:
                url = reverse('admin:students_student_change', args=[enrollment.student.pk])
                name = enrollment.student.user.get_full_name() or enrollment.student.user.username
                student_links.append(format_html('<a href="{}">{}</a>', url, name))
            return mark_safe('<br>'.join(student_links))
        return "No students enrolled"
    get_enrolled_students.short_description = 'Enrolled Students'
    
    def get_file_count(self, obj):
        count = obj.fileupload_set.count()
        return format_html('<span style="font-weight: bold;">{} files</span>', count)
    get_file_count.short_description = 'Uploaded Files'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'get_student_id', 'course', 'enrollment_date', 'is_active')
    list_filter = ('enrollment_date', 'is_active', 'course__difficulty', 'course__instructor')
    search_fields = ('student__user__username', 'student__user__first_name', 'student__user__last_name', 
                    'student__student_id', 'course__title')
    readonly_fields = ('enrollment_date',)
    list_editable = ('is_active',)
    date_hierarchy = 'enrollment_date'
    
    def has_add_permission(self, request):
        # Teachers/Admins can add enrollments
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        # Teachers/Admins can edit enrollments
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        # Teachers/Admins can delete enrollments
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        # Teachers/Admins can view enrollments
        return request.user.is_staff
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    get_student_name.short_description = 'Student Name'
    
    def get_student_id(self, obj):
        return obj.student.student_id
    get_student_id.short_description = 'Student ID'

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_file_name', 'uploaded_by', 'course', 'get_file_size', 'timestamp')
    list_filter = ('timestamp', 'course', 'course__difficulty')
    search_fields = ('title', 'description', 'uploaded_by__username', 'course__title')
    readonly_fields = ('timestamp', 'get_file_size', 'get_file_info')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('File Information', {
            'fields': ('title', 'description', 'file')
        }),
        ('Upload Details', {
            'fields': ('uploaded_by', 'course')
        }),
        ('File Statistics', {
            'fields': ('get_file_size', 'get_file_info', 'timestamp'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Teachers/Admins can add files
        return request.user.is_staff
    
    def has_change_permission(self, request, obj=None):
        # Teachers/Admins can edit files
        return request.user.is_staff
    
    def has_delete_permission(self, request, obj=None):
        # Teachers/Admins can delete files
        return request.user.is_staff
    
    def has_view_permission(self, request, obj=None):
        # Teachers/Admins can view files
        return request.user.is_staff
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Teachers can see all files, but could be restricted to their courses
        return qs
    
    def get_file_name(self, obj):
        return obj.get_file_name()
    get_file_name.short_description = 'File Name'
    
    def get_file_size(self, obj):
        size = obj.get_file_size()
        if size > 1024 * 1024:  # MB
            return f"{size / (1024 * 1024):.1f} MB"
        elif size > 1024:  # KB
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size} bytes"
    get_file_size.short_description = 'File Size'
    
    def get_file_info(self, obj):
        try:
            file_path = obj.file.path
            import os
            return format_html(
                'Path: {}<br>Exists: {}',
                file_path,
                'Yes' if os.path.exists(file_path) else 'No'
            )
        except:
            return "File information not available"
    get_file_info.short_description = 'File Details'

# Custom admin actions
def activate_courses(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_courses.short_description = "Activate selected courses"

def deactivate_courses(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_courses.short_description = "Deactivate selected courses"

def activate_enrollments(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_enrollments.short_description = "Activate selected enrollments"

def deactivate_enrollments(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_enrollments.short_description = "Deactivate selected enrollments"

# Add actions to admin classes
CourseAdmin.actions = [activate_courses, deactivate_courses]
EnrollmentAdmin.actions = [activate_enrollments, deactivate_enrollments]
