from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from students.models import Student, Course, Enrollment, FileUpload

class Command(BaseCommand):
    help = 'Create teacher group with appropriate permissions'

    def handle(self, *args, **options):
        # Create teacher group
        teacher_group, created = Group.objects.get_or_create(name='Teachers')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created Teachers group'))
        else:
            self.stdout.write(self.style.WARNING('Teachers group already exists'))
        
        # Define permissions for teachers
        permissions_to_add = [
            # Student permissions
            'view_student',
            'add_student', 
            'change_student',
            
            # Course permissions
            'view_course',
            'add_course',
            'change_course',
            'delete_course',
            
            # Enrollment permissions
            'view_enrollment',
            'add_enrollment',
            'change_enrollment',
            'delete_enrollment',
            
            # FileUpload permissions
            'view_fileupload',
            'add_fileupload',
            'change_fileupload',
            'delete_fileupload',
        ]
        
        # Get content types
        student_ct = ContentType.objects.get_for_model(Student)
        course_ct = ContentType.objects.get_for_model(Course)
        enrollment_ct = ContentType.objects.get_for_model(Enrollment)
        fileupload_ct = ContentType.objects.get_for_model(FileUpload)
        
        # Add permissions to teacher group
        for perm_codename in permissions_to_add:
            try:
                if 'student' in perm_codename:
                    permission = Permission.objects.get(codename=perm_codename, content_type=student_ct)
                elif 'course' in perm_codename:
                    permission = Permission.objects.get(codename=perm_codename, content_type=course_ct)
                elif 'enrollment' in perm_codename:
                    permission = Permission.objects.get(codename=perm_codename, content_type=enrollment_ct)
                elif 'fileupload' in perm_codename:
                    permission = Permission.objects.get(codename=perm_codename, content_type=fileupload_ct)
                else:
                    continue
                    
                teacher_group.permissions.add(permission)
                self.stdout.write(f'Added permission: {perm_codename}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Permission not found: {perm_codename}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully configured teacher group permissions'))
