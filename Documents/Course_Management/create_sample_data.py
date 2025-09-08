#!/usr/bin/env python3
"""
Sample data creation script for Course Management System
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_management.settings')
django.setup()

from django.contrib.auth.models import User
from students.models import Student, Course, Enrollment

def create_sample_data():
    print("Creating sample data for Course Management System...")
    
    # Create sample courses
    courses_data = [
        {
            'title': 'Introduction to Python Programming',
            'description': 'Learn the fundamentals of Python programming language. This course covers basic syntax, data types, control structures, functions, and object-oriented programming concepts.',
            'instructor': 'Dr. Sarah Johnson',
            'credits': 3,
            'difficulty': 'beginner',
            'max_students': 30,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date() + timedelta(days=90),
            'is_active': True
        },
        {
            'title': 'Web Development with Django',
            'description': 'Master web development using Django framework. Build dynamic web applications with models, views, templates, and user authentication.',
            'instructor': 'Prof. Michael Chen',
            'credits': 4,
            'difficulty': 'intermediate',
            'max_students': 25,
            'start_date': datetime.now().date() + timedelta(days=7),
            'end_date': datetime.now().date() + timedelta(days=120),
            'is_active': True
        },
        {
            'title': 'Data Science with Python',
            'description': 'Explore data science concepts using Python. Learn pandas, numpy, matplotlib, and machine learning basics.',
            'instructor': 'Dr. Emma Wilson',
            'credits': 4,
            'difficulty': 'intermediate',
            'max_students': 20,
            'start_date': datetime.now().date() + timedelta(days=14),
            'end_date': datetime.now().date() + timedelta(days=105),
            'is_active': True
        },
        {
            'title': 'Advanced Machine Learning',
            'description': 'Deep dive into machine learning algorithms and techniques. Covers neural networks, deep learning, and AI applications.',
            'instructor': 'Dr. Robert Davis',
            'credits': 5,
            'difficulty': 'advanced',
            'max_students': 15,
            'start_date': datetime.now().date() + timedelta(days=21),
            'end_date': datetime.now().date() + timedelta(days=150),
            'is_active': True
        },
        {
            'title': 'Database Design and SQL',
            'description': 'Learn database design principles and SQL programming. Covers normalization, indexing, and query optimization.',
            'instructor': 'Prof. Lisa Anderson',
            'credits': 3,
            'difficulty': 'beginner',
            'max_students': 35,
            'start_date': datetime.now().date() + timedelta(days=10),
            'end_date': datetime.now().date() + timedelta(days=80),
            'is_active': True
        },
        {
            'title': 'Mobile App Development',
            'description': 'Create mobile applications for iOS and Android platforms. Learn React Native and cross-platform development.',
            'instructor': 'Mr. James Taylor',
            'credits': 4,
            'difficulty': 'intermediate',
            'max_students': 22,
            'start_date': datetime.now().date() + timedelta(days=30),
            'end_date': datetime.now().date() + timedelta(days=120),
            'is_active': True
        },
        {
            'title': 'Cybersecurity Fundamentals',
            'description': 'Introduction to cybersecurity principles, threat analysis, and security best practices for modern applications.',
            'instructor': 'Dr. Alex Martinez',
            'credits': 3,
            'difficulty': 'beginner',
            'max_students': 28,
            'start_date': datetime.now().date() + timedelta(days=5),
            'end_date': datetime.now().date() + timedelta(days=95),
            'is_active': True
        },
        {
            'title': 'Cloud Computing with AWS',
            'description': 'Master cloud computing concepts using Amazon Web Services. Learn deployment, scaling, and cloud architecture.',
            'instructor': 'Ms. Jennifer Lee',
            'credits': 4,
            'difficulty': 'advanced',
            'max_students': 18,
            'start_date': datetime.now().date() + timedelta(days=28),
            'end_date': datetime.now().date() + timedelta(days=135),
            'is_active': True
        }
    ]
    
    # Create courses
    created_courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults=course_data
        )
        if created:
            print(f"Created course: {course.title}")
            created_courses.append(course)
        else:
            print(f"Course already exists: {course.title}")
    
    # Create sample students
    students_data = [
        {
            'username': 'student1',
            'email': 'student1@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'student_id': 'STU001',
            'phone_number': '123-456-7890'
        },
        {
            'username': 'student2',
            'email': 'student2@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'student_id': 'STU002',
            'phone_number': '234-567-8901'
        },
        {
            'username': 'student3',
            'email': 'student3@example.com',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'student_id': 'STU003',
            'phone_number': '345-678-9012'
        }
    ]
    
    # Create student users and profiles
    for student_data in students_data:
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name'],
                'is_active': True
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.username}")
            
            # Create student profile
            student, student_created = Student.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': student_data['student_id'],
                    'phone_number': student_data['phone_number']
                }
            )
            
            if student_created:
                print(f"Created student profile: {student.student_id}")
                
                # Enroll student in some courses
                available_courses = Course.objects.filter(is_active=True)[:3]
                for course in available_courses:
                    enrollment, enroll_created = Enrollment.objects.get_or_create(
                        student=student,
                        course=course,
                        defaults={'is_active': True}
                    )
                    if enroll_created:
                        print(f"Enrolled {student.user.username} in {course.title}")
        else:
            print(f"User already exists: {user.username}")
    
    print("\nSample data creation completed!")
    print("\nCreated accounts:")
    print("- Admin: admin/admin123")
    print("- Student 1: student1/password123")
    print("- Student 2: student2/password123")
    print("- Student 3: student3/password123")
    print(f"\nTotal courses: {Course.objects.count()}")
    print(f"Total students: {Student.objects.count()}")
    print(f"Total enrollments: {Enrollment.objects.count()}")

if __name__ == '__main__':
    create_sample_data()
