from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course, Subject
from teachers.models import Teacher
from batches.models import Batch
from students.models import Student
from announcements.models import Announcement
from website.models import Gallery, Testimonial, FAQ
from .forms import PublicAdmissionForm, PublicContactForm

def home(request):
    """Homepage with all 15 rich sections."""
    courses = Course.objects.filter(is_active=True)
    cbse_courses = courses.filter(board='CBSE')[:6]
    bihar_courses = []
    teachers = Teacher.objects.filter(is_active=True)[:4]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    announcements = Announcement.objects.filter(is_active=True, target_audience__in=['all', 'batch']).order_by('-created_at')[:4]
    gallery_items = Gallery.objects.filter(is_active=True)[:6]
    faqs = FAQ.objects.filter(is_active=True)[:4]

    # Dynamic statistics
    stats = {
        'total_students': Student.objects.filter(is_active=True).count() or 150,
        'total_teachers': Teacher.objects.filter(is_active=True).count() or 12,
        'total_courses': courses.count() or 14,
        'total_batches': Batch.objects.filter(status='active').count() or 18,
    }

    # Handle quick admission inquiry on home
    if request.method == 'POST' and 'admission_submit' in request.POST:
        admission_form = PublicAdmissionForm(request.POST)
        if admission_form.is_valid():
            admission_form.save()
            messages.success(request, 'Thank you! Your admission enquiry has been submitted. Our team will contact you shortly.')
            return redirect('website:home')
    else:
        admission_form = PublicAdmissionForm()

    context = {
        'cbse_courses': cbse_courses,
        'bihar_courses': bihar_courses,
        'teachers': teachers,
        'testimonials': testimonials,
        'announcements': announcements,
        'gallery_items': gallery_items,
        'faqs': faqs,
        'stats': stats,
        'admission_form': admission_form,
    }
    return render(request, 'website/home.html', context)

def about(request):
    """About Us page."""
    teachers_count = Teacher.objects.filter(is_active=True).count()
    students_count = Student.objects.filter(is_active=True).count()
    courses_count = Course.objects.filter(is_active=True).count()
    
    context = {
        'teachers_count': teachers_count,
        'students_count': students_count,
        'courses_count': courses_count,
    }
    return render(request, 'website/about.html', context)

def courses_list(request):
    """Course catalog with filters."""
    board_filter = request.GET.get('board', '')
    class_filter = request.GET.get('class', '')
    search_query = request.GET.get('q', '')

    courses = Course.objects.filter(is_active=True)
    if board_filter:
        courses = courses.filter(board=board_filter)
    if class_filter:
        courses = courses.filter(class_level=class_filter)
    if search_query:
        courses = courses.filter(name__icontains=search_query)

    context = {
        'courses': courses,
        'selected_board': board_filter,
        'selected_class': class_filter,
        'search_query': search_query,
    }
    return render(request, 'website/courses.html', context)

def course_detail(request, pk):
    """Single course detail view."""
    course = get_object_or_404(Course, pk=pk)
    related_batches = Batch.objects.filter(course=course, status='active')
    related_courses = Course.objects.filter(board=course.board, is_active=True).exclude(pk=pk)[:3]
    
    context = {
        'course': course,
        'batches': related_batches,
        'related_courses': related_courses,
    }
    return render(request, 'website/course_detail.html', context)

def teachers_list(request):
    """Faculty & Staff public listing."""
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'website/teachers.html', {'teachers': teachers})

def gallery_view(request):
    """Gallery page redirect."""
    return redirect('website:home')

def contact_view(request):
    """Contact page with message form."""
    if request.method == 'POST':
        form = PublicContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent to NS Classes. We will respond soon.')
            return redirect('website:contact')
    else:
        form = PublicContactForm()
    return render(request, 'website/contact.html', {'form': form})

def admission_view(request):
    """Admission enquiry page."""
    if request.method == 'POST':
        form = PublicAdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admission enquiry submitted successfully! NS Classes will reach out to you within 24 hours.')
            return redirect('website:admission')
    else:
        # Pre-fill interested course from GET param if available
        initial_data = {}
        course_name = request.GET.get('course', '')
        if course_name:
            initial_data['interested_course'] = course_name
        form = PublicAdmissionForm(initial=initial_data)
    return render(request, 'website/admission.html', {'form': form})

def faq_view(request):
    """Frequently Asked Questions."""
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'website/faq.html', {'faqs': faqs})

def privacy_policy(request):
    """Privacy Policy page."""
    return render(request, 'website/privacy.html')

def terms_conditions(request):
    """Terms and Conditions page."""
    return render(request, 'website/terms.html')
