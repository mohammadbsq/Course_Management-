# Django Student Course Management System

**Project:** Complete Course Management System  
**Date:** July 3, 2025

## Project Overview

This is a comprehensive Django web application for managing student course enrollments and file sharing. The system allows students to register, enroll in courses, and manage course-related files, while providing administrators with tools to manage courses and student information.

## Features

### Student Features
- User registration and authentication
- Browse and enroll in available courses
- View enrolled courses dashboard
- Upload, download, and delete files for enrolled courses
- Maximum 5 course enrollment limit per student
- Responsive design for mobile and desktop

### Admin Features
- Manage students and courses through Django admin panel
- View all enrollments and file uploads
- Full CRUD operations on all models
- Advanced filtering and search capabilities

### Security Features
- Login required for sensitive operations
- File access restricted to enrolled students only
- File deletion restricted to uploader or admin
- CSRF protection on all forms
- Proper permission checks throughout the application

## Technology Stack

- **Backend:** Django 4.2.7
- **Database:** SQLite (default, easily configurable)
- **Frontend:** Bootstrap 5.3, HTML5, CSS3, JavaScript
- **File Handling:** Django FileField with custom upload paths
- **Authentication:** Django built-in authentication system

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- pip package manager

### 2. Clone and Setup Virtual Environment
```bash
# Navigate to project directory
cd /home/csen/Course_Management

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Create Sample Data (Optional)
```bash
python manage.py shell
```

Then run the following Python code to create sample courses:
```python
from students.models import Course
from datetime import date, timedelta

# Create sample courses
courses = [
    {
        'title': 'Introduction to Python Programming',
        'description': 'Learn the fundamentals of Python programming language, including syntax, data structures, and basic algorithms.',
        'instructor': 'Dr. Sarah Johnson',
        'credits': 3,
        'difficulty': 'beginner',
        'max_students': 25,
        'start_date': date.today(),
        'end_date': date.today() + timedelta(days=90),
    },
    {
        'title': 'Web Development with Django',
        'description': 'Build dynamic web applications using Django framework, covering models, views, templates, and deployment.',
        'instructor': 'Prof. Michael Chen',
        'credits': 4,
        'difficulty': 'intermediate',
        'max_students': 20,
        'start_date': date.today() + timedelta(days=7),
        'end_date': date.today() + timedelta(days=120),
    },
    {
        'title': 'Data Science and Machine Learning',
        'description': 'Explore data analysis, visualization, and machine learning techniques using Python and popular libraries.',
        'instructor': 'Dr. Emily Rodriguez',
        'credits': 4,
        'difficulty': 'advanced',
        'max_students': 15,
        'start_date': date.today() + timedelta(days=14),
        'end_date': date.today() + timedelta(days=150),
    },
]

for course_data in courses:
    Course.objects.create(**course_data)

print("Sample courses created successfully!")
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
- **Main site:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/
- **Student Registration:** http://127.0.0.1:8000/register/

## Project Structure

```
course_management/
├── course_management/          # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI configuration
├── students/                   # Main application
│   ├── models.py              # Database models
│   ├── views.py               # Business logic
│   ├── forms.py               # Form handling
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin configuration
│   └── migrations/            # Database migrations
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── registration/          # Authentication templates
│   └── students/              # Student-specific templates
├── static/                     # Static files
│   ├── css/style.css          # Custom CSS
│   └── js/main.js             # JavaScript functionality
├── media/                      # User uploads
│   └── uploads/               # Course files
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Database Models

### 1. Student Model
- Extends Django User with additional fields
- `student_id`: Unique identifier
- `phone_number`: Contact information
- `date_of_birth`: Optional birth date
- `can_enroll_more_courses()`: Method to check enrollment limit

### 2. Course Model
- `title`: Course name
- `description`: Course description
- `instructor`: Teacher name
- `credits`: Credit hours
- `difficulty`: Beginner/Intermediate/Advanced
- `max_students`: Enrollment limit
- `start_date` and `end_date`: Course duration
- `is_active`: Status flag

### 3. Enrollment Model
- Links students to courses
- Prevents duplicate enrollments
- Tracks enrollment date and status

### 4. FileUpload Model
- Manages file uploads per course
- Tracks uploader and upload date
- Organized by course folders

## Key Features Implemented

### Authentication & Authorization
- ✅ User registration with student profile creation
- ✅ Login/logout functionality
- ✅ Permission-based access control
- ✅ Session management

### Course Management
- ✅ Course listing with filtering
- ✅ Course details view
- ✅ Enrollment system with limits
- ✅ My courses dashboard

### File Management
- ✅ File upload for enrolled courses
- ✅ File download with permission checks
- ✅ File deletion (owner or admin only)
- ✅ Organized file storage by course

### User Interface
- ✅ Responsive Bootstrap design
- ✅ Interactive JavaScript enhancements
- ✅ Form validation and error handling
- ✅ Success/error message system

### Admin Panel
- ✅ Custom admin interfaces for all models
- ✅ Advanced filtering and search
- ✅ Bulk operations support

## Testing Scenarios

1. **User Registration:**
   - Register a new student account
   - Verify email validation
   - Check student profile creation

2. **Course Enrollment:**
   - Browse available courses
   - Test enrollment limits (5 courses max)
   - Verify duplicate enrollment prevention

3. **File Management:**
   - Upload files to enrolled courses
   - Download files from courses
   - Test file deletion permissions

4. **Admin Functions:**
   - Create and manage courses
   - View student enrollments
   - Manage file uploads

## Security Considerations

- All views require appropriate permissions
- File access is restricted to enrolled students
- CSRF protection on all forms
- SQL injection prevention through Django ORM
- XSS protection through template escaping

## Future Enhancements

- Email notifications for enrollments
- Grade management system
- Discussion forums per course
- Calendar integration
- Mobile app development
- API endpoints for external integration

## Troubleshooting

### Common Issues

1. **Migration Errors:**
   ```bash
   python manage.py makemigrations --empty students
   python manage.py migrate
   ```

2. **Static Files Not Loading:**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Errors:**
   - Check file permissions in media directory
   - Ensure proper ownership of uploaded files

### Development Tips

- Use `DEBUG = True` for development
- Check Django logs for detailed error messages
- Use Django shell for debugging: `python manage.py shell`
- Monitor database queries with Django Debug Toolbar

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes and is free to use and modify.

---

**Contact:** For questions or support, please refer to the project documentation or create an issue in the repository.
