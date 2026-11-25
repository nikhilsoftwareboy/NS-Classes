from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance
from batches.models import Batch
from students.models import Student

def is_staff_or_teacher(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['admin', 'teacher'])

@login_required
def mark_attendance(request):
    """Mark attendance for students in a batch for a specific date."""
    if not is_staff_or_teacher(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    today_str = timezone.now().strftime('%Y-%m-%d')
    date_str = request.GET.get('date', today_str)
    batch_id = request.GET.get('batch')

    # If teacher, show their batches first
    teacher = getattr(request.user, 'teacher_profile', None)
    if teacher and not request.user.is_superuser:
        batches = Batch.objects.filter(teacher=teacher, status='active')
    else:
        batches = Batch.objects.filter(status='active')

    selected_batch = None
    if batch_id:
        selected_batch = get_object_or_404(Batch, pk=batch_id)
    elif batches.exists():
        selected_batch = batches.first()

    students_attendance = []
    if selected_batch:
        students = Student.objects.filter(batch=selected_batch, is_active=True).select_related('user')
        # Existing records for this batch & date
        existing_records = {att.student_id: att.status for att in Attendance.objects.filter(batch=selected_batch, date=date_str)}

        for st in students:
            status = existing_records.get(st.id, 'present')
            students_attendance.append({
                'student': st,
                'status': status
            })

    if request.method == 'POST':
        action = request.POST.get('save_attendance')
        if action and selected_batch:
            date_val = request.POST.get('attendance_date', date_str)
            for item in students_attendance:
                st_id = item['student'].id
                submitted_status = request.POST.get(f"status_{st_id}", 'present')
                Attendance.objects.update_or_create(
                    student=item['student'],
                    batch=selected_batch,
                    date=date_val,
                    defaults={
                        'status': submitted_status,
                        'marked_by': request.user
                    }
                )
            messages.success(request, f"Attendance for {selected_batch.name} on {date_val} saved successfully!")
            return redirect(f"/attendance/mark/?batch={selected_batch.id}&date={date_val}")

    context = {
        'batches': batches,
        'selected_batch': selected_batch,
        'selected_date': date_str,
        'students_attendance': students_attendance,
        'today_str': today_str,
    }
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
def attendance_report(request):
    """View overall attendance summary and statistics."""
    if not is_staff_or_teacher(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    batches = Batch.objects.filter(status='active')
    batch_id = request.GET.get('batch')
    
    selected_batch = None
    student_stats = []

    if batch_id:
        selected_batch = get_object_or_404(Batch, pk=batch_id)
        students = Student.objects.filter(batch=selected_batch, is_active=True).select_related('user')
        for st in students:
            total = Attendance.objects.filter(student=st, batch=selected_batch).count()
            present = Attendance.objects.filter(student=st, batch=selected_batch, status='present').count()
            absent = total - present
            pct = round((present / total * 100), 1) if total > 0 else 0
            student_stats.append({
                'student': st,
                'total': total,
                'present': present,
                'absent': absent,
                'percentage': pct,
            })

    context = {
        'batches': batches,
        'selected_batch': selected_batch,
        'student_stats': student_stats,
    }
    return render(request, 'attendance/attendance_report.html', context)
