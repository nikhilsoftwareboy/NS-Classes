from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q

from accounts.models import UserProfile
from students.models import Student
from teachers.models import Teacher
from courses.models import Course
from batches.models import Batch
from timetable.models import TimetableEntry
from attendance.models import Attendance
from fees.models import FeeRecord
from enquiries.models import AdmissionEnquiry, ContactMessage
from materials.models import StudyMaterial
from announcements.models import Announcement


@login_required
def dashboard_home(request):
    """Central router to redirect user to their respective dashboard."""
    user = request.user
    if user.is_superuser:
        return redirect('dashboard:admin_dashboard')
    
    try:
        role = user.profile.role
    except Exception:
        role = 'student'

    if role == 'admin':
        return redirect('dashboard:admin_dashboard')
    elif role == 'teacher':
        return redirect('dashboard:teacher_dashboard')
    else:
        return redirect('dashboard:student_dashboard')


@login_required
def admin_dashboard(request):
    """Super Admin / Director Dashboard."""
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'admin')):
        messages.error(request, "Access restricted to Administrator / Director only.")
        return redirect('dashboard:home')

    today = timezone.now().date()
    
    # Core Metrics
    total_students = Student.objects.filter(is_active=True).count()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_batches = Batch.objects.filter(status='active').count()
    
    # Today Attendance
    today_attendance_count = Attendance.objects.filter(date=today).count()
    today_present_count = Attendance.objects.filter(date=today, status='present').count()
    
    # Fees summary
    fee_agg = FeeRecord.objects.aggregate(
        total_expected=Sum('total_fee'),
        total_collected=Sum('paid_amount')
    )
    total_expected = fee_agg['total_expected'] or 0
    total_collected = fee_agg['total_collected'] or 0
    pending_fees_total = total_expected - total_collected
    pending_fee_records = FeeRecord.objects.filter(status__in=['pending', 'partial', 'overdue']).count()

    # Enquiries
    new_enquiries_count = AdmissionEnquiry.objects.filter(status='new').count()
    unread_messages_count = ContactMessage.objects.filter(is_read=False).count()

    # Recent Data
    recent_students = Student.objects.select_related('user', 'batch', 'course').order_by('-created_at')[:6]
    recent_enquiries = AdmissionEnquiry.objects.order_by('-created_at')[:6]
    recent_announcements = Announcement.objects.order_by('-created_at')[:5]
    recent_fee_payments = FeeRecord.objects.select_related('student__user').order_by('-updated_at')[:6]
    
    # Today's Timetable
    current_day = timezone.now().strftime('%A')
    today_classes = TimetableEntry.objects.filter(day=current_day).select_related('batch', 'subject', 'teacher__user').order_by('start_time')[:8]

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_batches': total_batches,
        'today_attendance_count': today_attendance_count,
        'today_present_count': today_present_count,
        'total_collected': total_collected,
        'pending_fees_total': pending_fees_total,
        'pending_fee_records': pending_fee_records,
        'new_enquiries_count': new_enquiries_count,
        'unread_messages_count': unread_messages_count,
        'recent_students': recent_students,
        'recent_enquiries': recent_enquiries,
        'recent_announcements': recent_announcements,
        'recent_fee_payments': recent_fee_payments,
        'today_classes': today_classes,
        'current_day': current_day,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    """Teacher Dashboard."""
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher and not request.user.is_superuser:
        messages.error(request, "Teacher profile not found for this account.")
        return redirect('dashboard:home')

    today = timezone.now().date()
    current_day = timezone.now().strftime('%A')

    if teacher:
        assigned_batches = Batch.objects.filter(teacher=teacher)
        today_timetable = TimetableEntry.objects.filter(teacher=teacher, day=current_day).order_by('start_time')
        full_timetable = TimetableEntry.objects.filter(teacher=teacher).order_by('day', 'start_time')
        uploaded_materials = StudyMaterial.objects.filter(uploaded_by=request.user).order_by('-upload_date')[:6]
        announcements = Announcement.objects.filter(Q(target_audience='teachers') | Q(target_audience='all') | Q(created_by=request.user)).order_by('-created_at')[:6]
        total_students = Student.objects.filter(batch__teacher=teacher, is_active=True).count()
    else:
        assigned_batches = Batch.objects.all()[:5]
        today_timetable = TimetableEntry.objects.filter(day=current_day)[:5]
        full_timetable = TimetableEntry.objects.all()[:10]
        uploaded_materials = StudyMaterial.objects.all()[:6]
        announcements = Announcement.objects.all()[:6]
        total_students = Student.objects.filter(is_active=True).count()

    context = {
        'teacher': teacher,
        'assigned_batches': assigned_batches,
        'today_timetable': today_timetable,
        'full_timetable': full_timetable,
        'uploaded_materials': uploaded_materials,
        'announcements': announcements,
        'total_students': total_students,
        'current_day': current_day,
        'today': today,
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    """Student Dashboard."""
    student = getattr(request.user, 'student_profile', None)
    
    # Calculate Attendance
    total_classes = 0
    present_classes = 0
    absent_classes = 0
    attendance_pct = 0
    batch_timetable = []
    study_materials = []
    announcements = []
    fee_records = []

    if student:
        attendance_qs = Attendance.objects.filter(student=student)
        total_classes = attendance_qs.count()
        present_classes = attendance_qs.filter(status='present').count()
        absent_classes = attendance_qs.filter(status='absent').count()
        if total_classes > 0:
            attendance_pct = round((present_classes / total_classes) * 100, 1)

        if student.batch:
            batch_timetable = TimetableEntry.objects.filter(batch=student.batch).order_by('day', 'start_time')
            study_materials = StudyMaterial.objects.filter(
                Q(batch=student.batch) | 
                Q(board=student.board, class_level=student.class_level) |
                Q(batch__isnull=True, class_level=student.class_level)
            ).distinct().order_by('-upload_date')[:8]

            announcements = Announcement.objects.filter(
                Q(target_audience='all') | 
                Q(target_audience='batch', batch=student.batch)
            ).filter(is_active=True).order_by('-created_at')[:6]
        else:
            announcements = Announcement.objects.filter(target_audience='all', is_active=True).order_by('-created_at')[:6]

        fee_records = FeeRecord.objects.filter(student=student).order_by('-created_at')

    context = {
        'student': student,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'absent_classes': absent_classes,
        'attendance_pct': attendance_pct,
        'batch_timetable': batch_timetable,
        'study_materials': study_materials,
        'announcements': announcements,
        'fee_records': fee_records,
    }
    return render(request, 'dashboard/student_dashboard.html', context)
