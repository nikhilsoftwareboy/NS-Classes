# NS Classes — Complete Django Coaching Institute Management System

**Directors:** Nikhil Kumar Singh & Saurabh Raj  
**Contact / Helpline:** +91 987654321  
**Education Boards:** CBSE Board (Class 6 - 12)  
**Tagline:** "Your Success Begins Here"  

---

## 📖 About the Project

**NS Classes** is a complete, production-ready, modern, and responsive Coaching Institute Management Web Application built with **Python 3**, **Django**, **Bootstrap 5**, and **SQLite/PostgreSQL/MySQL**.

The system provides:
1. **Public-Facing Website** with 15 rich sections (Hero, About Us, Directors' Message, Courses for CBSE Board, Faculty Profiles, Dynamic Statistics, Gallery, Testimonials, FAQ, and Admission Enquiry & Contact Forms).
2. **Super Admin / Director Console** with institutional analytics, Chart.js graphs, student management, batch allocation, separate timetable scheduling per batch, daily attendance tracking, fee management with printable official numbered receipts, admission lead management, and study material uploads.
3. **Teacher Portal** for faculty to view assigned batches, daily & weekly timetable, take batch attendance (with instant "Mark All Present/Absent" shortcuts), upload PDF study materials, and broadcast batch announcements.
4. **Student Portal** providing students with individual student ID cards, batch allocation details, assigned batch timetable, attendance percentage tracker, fee payment records with receipt viewing, downloadable study notes, and important board notices.

---

## 🛠 Technology Stack

- **Backend:** Python, Django 5 (Django ORM, Authentication, Messages Framework, File Uploads)
- **Database:** SQLite (default for development; easily configurable for PostgreSQL/MySQL in `config/settings.py`)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons, Google Fonts (Outfit & Inter), Chart.js
- **Architecture:** Modular Django App structure with 12 distinct apps.

---

## 📂 Project Architecture

```
NS classes/
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/         # User roles (admin, teacher, student), login, registration, profiles
├── website/          # Public website pages, CMS (Gallery, Testimonials, FAQ), context processors
├── dashboard/        # Role-based dashboards (Director, Teacher, Student)
├── courses/          # Courses & Subjects management
├── batches/          # Batch management & student assignment
├── timetable/        # Separate timetable scheduling per batch
├── students/         # Student database & profiles
├── teachers/         # Faculty & teacher profiles
├── attendance/       # Batch attendance marking & analytics reports
├── fees/             # Fee tracking, installment recording, printable receipts
├── enquiries/        # Online admission enquiries & contact messages
├── materials/        # PDF notes & study resources repository
├── announcements/    # Broadcast notices & targeted announcements
├── templates/        # Clean HTML5 + Bootstrap 5 templates
├── static/           # Custom CSS & JS files
└── media/            # Uploaded photos, documents & notes
```

---

## 👥 Default Demo User Credentials

Run `python manage.py load_sample_data` to automatically create all sample courses, batches, timetables, and user accounts:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Director / Super Admin** | `admin` | `admin123` | Full administrative control |
| **Director / Teacher** | `pinku_raj` (or `saurabh_raj`) | `teacher@123` | Mathematics & Physics Faculty / Directors |
| **Faculty Teacher** | `amit_sharma` | `teacher@123` | Physics Senior Faculty |
| **Faculty Teacher** | `priya_verma` | `teacher@123` | Chemistry Expert Faculty |
| **CBSE Class 10 Student** | `ns_stu_001` | `student@123` | Rohan Kumar (CBSE Class 10) |
| **CBSE Class 10 Student** | `ns_stu_006` | `student@123` | Anjali Gupta (CBSE Class 10) |
| **CBSE Class 12 Student** | `ns_stu_004` | `student@123` | Pooja Singh (CBSE Class 12) |

---

## 🚀 Setup & Installation Instructions

### 1. Create and activate a virtual environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Load realistic sample data (Courses, Batches, Timetables, Users)

```bash
python manage.py load_sample_data
```

*(Optional: You can also create a custom superuser using `python manage.py createsuperuser`)*

### 5. Start the development server

```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Public Website:** `http://127.0.0.1:8000/`
- **Portal Login:** `http://127.0.0.1:8000/login/`
- **Director / Admin Dashboard:** `http://127.0.0.1:8000/dashboard/`
- **Django Built-in Admin:** `http://127.0.0.1:8000/django-admin/`

---

## 🌐 Complete URL Sitemap

### Public Website
- `/` — Homepage (Hero, About, Why Choose Us, Courses, Faculty, Stats, Testimonials, Notices, Gallery, CTA)
- `/about/` — About Us & Directors' Message (Nikhil Kumar Singh & Saurabh Raj)
- `/courses/` — Filterable Course Catalog (CBSE Board Class 6 to 12)
- `/courses/<id>/` — Single Course Detailed Syllabus & Batches
- `/teachers/` — Faculty & Teaching Staff Profiles
- `/gallery/` — Categorized Photo Gallery
- `/contact/` — Contact Page with Call Now, WhatsApp, & Message Form
- `/admission/` — Online Admission Application Form
- `/faq/` — Frequently Asked Questions
- `/privacy/` — Privacy Policy
- `/terms/` — Terms and Conditions

### Authentication & Portals
- `/login/` — Universal Role-Based Login
- `/register/` — Student Portal Registration
- `/logout/` — Logout
- `/profile/` — User Profile Settings & Photo Upload
- `/dashboard/` — Intelligent Role-based Redirection
- `/admin/dashboard/` — Director / Super Admin Console
- `/teacher/dashboard/` — Teacher Portal
- `/student/dashboard/` — Student Portal

### Management Modules
- `/students/` — Student Database, Search, Filter by Board/Class/Batch, Add/Edit/Delete
- `/manage-teachers/` — Teacher Faculty Management
- `/manage-courses/` — Course & Subject Management
- `/batches/` — Batch Creation, Capacity Tracking, Student Allocation
- `/timetable/` — Separate Timetable Scheduling & 7-Day Grid per Batch
- `/attendance/mark/` — Daily Batch Attendance Marking
- `/attendance/report/` — Batch Attendance Summary Report
- `/fees/` — Fee Records, Dues Tracker, Installment Recorder
- `/fees/<id>/receipt/` — Official Printable Fee Receipt
- `/enquiries/` — Admission Leads & Status Tracker
- `/enquiries/messages/` — Contact Message Inbox
- `/materials/` — PDF Notes & Study Resources Repository
- `/announcements/` — Broadcast Notices with Audience & Priority Controls

---

## 🛡 Security & Best Practices

- **CSRF Protection:** Enabled on all forms with `{% csrf_token %}`.
- **Authorization:** `login_required` decorators and role verification preventing unauthorized access or cross-student record visibility.
- **Password Security:** Django PBKDF2 with SHA256 password hashing.
- **Data Integrity:** Foreign key constraints, cascade protections, and unique attendance record constraints `['student', 'date', 'batch']`.

---

© 2026 **NS Classes**. Directed by **Nikhil Kumar Singh & Saurabh Raj**. Helpline: **+91 987654321**.
