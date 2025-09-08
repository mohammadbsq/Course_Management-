# Course Management System

A comprehensive Django-based course management system for educational institutions.

**Student Name**: [Your Name]  
**Student ID**: [Your Student ID]

## Features

- **Student Registration & Authentication**: Students can register, login, and manage their profiles
- **Admin Registration**: Administrators can register with elevated privileges
- **Course Management**: Admins can add, edit, and manage courses through the admin interface
- **Course Enrollment**: Students can enroll in courses (maximum 5 courses per student)
- **File Management**: Upload, download, and delete course-related files
- **User-Friendly Interface**: Modern, responsive design with Bootstrap
- **Admin Panel**: Comprehensive admin interface for managing all aspects of the system

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or extract the project**
   ```bash
   cd Course_Management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create sample data (optional)**
   ```bash
   python create_sample_data.py
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage

### For Students
1. Register for a new account via "Student Registration"
2. Login with your credentials
3. Browse available courses
4. Enroll in courses (up to 5 courses)
5. Upload files for your enrolled courses
6. Download course materials
7. Delete files you uploaded

### For Admins
1. Register for admin account via "Admin Registration" or use existing admin account
2. Access the admin panel at /admin/
3. Add and manage courses
4. Manage student information
5. Monitor enrollments
6. View uploaded files

### Sample Accounts (if sample data is created)
- **Admin**: admin/admin123
- **Student 1**: student1/password123
- **Student 2**: student2/password123
- **Student 3**: student3/password123

## Project Structure

```
course_management/
├── course_management/          # Project configuration
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # Project URLs
│   └── wsgi.py
├── students/                   # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── forms.py               # Django forms
│   ├── admin.py               # Admin configuration
│   └── urls.py                # App URLs
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── registration/          # Authentication templates
│   └── students/              # Student app templates
├── static/                     # CSS and JavaScript files
├── media/                      # User uploaded files
├── manage.py                   # Django management script
├── requirements.txt           # Python dependencies
└── create_sample_data.py      # Sample data creation script
```

## Models

- **Student**: Extends Django User model with student-specific fields
- **Course**: Represents courses with title, description, instructor, difficulty, etc.
- **Enrollment**: Links students to courses with enrollment date and status
- **FileUpload**: Handles file uploads for courses with metadata

## URL Configuration

### Project Level (`course_management/urls.py`)
- Admin URLs
- Student app URLs
- Media file serving

### App Level (`students/urls.py`)
- Student registration
- Admin registration
- Course listing and details
- Enrollment
- File upload/download/delete

## Views

- **Function-based views** for all operations
- **@login_required** decorators for protected views
- **Permission checking** for file operations
- **Django messages framework** for user feedback

## Forms

- **StudentRegistrationForm**: Django ModelForm for student registration
- **AdminRegistrationForm**: Django ModelForm for admin registration
- **CourseEnrollmentForm**: Form for course enrollment
- **FileUploadForm**: Form for file uploads

## Authentication & Authorization

- Django's built-in authentication system
- User login/logout functionality
- Permission-based access control
- File access restrictions (only enrolled students)
- File deletion restrictions (only uploader or admin)

## Admin Panel Customization

- Custom admin interface for all models
- Enhanced list displays with custom fields
- Search and filter functionality
- Bulk actions for course/enrollment management
- Inline editing capabilities

## Security Features

- CSRF protection on all forms
- User authentication required for sensitive operations
- File access control (only enrolled students can access course files)
- Permission-based file deletion (users can only delete their own files)
- Admin-only course management

## Technical Restrictions Implemented

- Students can enroll in maximum 5 courses
- Only file uploader or admin can delete files
- @login_required decorators protect sensitive views
- Proper permission checking throughout the application

## Technologies Used

- **Django 4.2.7** - Web framework
- **Python 3.x** - Programming language
- **Bootstrap 5** - CSS framework
- **Font Awesome** - Icons
- **SQLite** - Database (default)
- **Pillow** - Image processing

## License

This project is for educational purposes.
