#!/usr/bin/env python3
"""
Test script to create a teacher account
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

from django.contrib.auth.models import User, Group

def create_test_teacher():
    print("Creating test teacher account...")
    
    try:
        # Create teacher account
        teacher = User.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='teacher123',
            first_name='John',
            last_name='Teacher',
            is_staff=True
        )
        
        # Add to Teachers group
        teachers_group = Group.objects.get(name='Teachers')
        teacher.groups.add(teachers_group)
        
        print(f'✓ Created teacher account: {teacher.username}')
        print(f'✓ Is staff: {teacher.is_staff}')
        print(f'✓ Is superuser: {teacher.is_superuser}')
        print(f'✓ Groups: {[g.name for g in teacher.groups.all()]}')
        print(f'✓ Has {teacher.get_all_permissions().__len__()} permissions')
        
        return teacher
        
    except Exception as e:
        print(f'✗ Error creating teacher: {e}')
        return None

if __name__ == "__main__":
    create_test_teacher()
