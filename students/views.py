from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from accounts.models import UserProfile
from .models import Student
from .forms import StudentForm
from batches.models import Batch
from courses.models import Course
from fees.models import FeeRecord
from attendance.models import Attendance

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

@login_required
def student_list(request):
    """List, filter, and search students (admin and teachers)."""
    if not (is_admin(request.user) or (hasattr(request.user, 'profile') and request.user.profile.role == 'teacher')):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    students = Student.objects.select_related('user', 'batch', 'course').all()

    # Search and Filter
    q = request.GET.get('q', '')
    board = request.GET.get('board', '')
    class_level = request.GET.get('class', '')
    batch_id = request.GET.get('batch', '')
    course_id = request.GET.get('course', '')

    if q:
        students = students.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(student_id__icontains=q) |
            Q(roll_number__icontains=q) |
            Q(phone__icontains=q) |
            Q(father_name__icontains=q)
        )
    if board:
        students = students.filter(board=board)
    if class_level:
        students = students.filter(class_level=class_level)
    if batch_id:
        students = students.filter(batch_id=batch_id)
    if course_id:
        students = students.filter(course_id=course_id)

    batches = Batch.objects.filter(status='active')
    courses = Course.objects.filter(is_active=True)

    context = {
        'students': students,
        'batches': batches,
        'courses': courses,
        'q': q,
        'selected_board': board,
        'selected_class': class_level,
        'selected_batch': batch_id,
        'selected_course': course_id,
        'total_count': students.count(),
    }
    return render(request, 'students/student_list.html', context)

@login_required
def student_detail(request, pk):
    """View complete profile of a student."""
    student = get_object_or_404(Student.objects.select_related('user', 'batch', 'course'), pk=pk)
    
    # Students can only view their own profile
    if hasattr(request.user, 'student_profile') and not is_admin(request.user) and request.user.student_profile != student:
        messages.error(request, "You can only view your own profile.")
        return redirect('dashboard:student_dashboard')

    fee_records = FeeRecord.objects.filter(student=student)
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')[:15]
    total_attendance = Attendance.objects.filter(student=student).count()
    present_attendance = Attendance.objects.filter(student=student, status='present').count()
    pct = round((present_attendance / total_attendance * 100), 1) if total_attendance else 0

    context = {
        'student': student,
        'fee_records': fee_records,
        'attendance_records': attendance_records,
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'attendance_pct': pct,
    }
    return render(request, 'students/student_detail.html', context)

@login_required
def student_create(request):
    """Admin creates a new student along with User account."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user account
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data.get('last_name') or ''
            username = form.cleaned_data.get('username') or form.cleaned_data['student_id'].lower().replace('-', '_')
            email = form.cleaned_data.get('email') or f"{username}@nsclasses.edu"
            password = form.cleaned_data.get('password') or 'student@123'

            if User.objects.filter(username=username).exists():
                messages.error(request, f"Username '{username}' already exists. Please choose a different one.")
                return render(request, 'students/student_form.html', {'form': form, 'title': 'Add New Student'})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            UserProfile.objects.create(user=user, role='student', phone=form.cleaned_data.get('phone', ''))

            student = form.save(commit=False)
            student.user = user
            student.save()

            # If course is selected and has fee, create an initial FeeRecord
            if student.course and student.course.fees:
                FeeRecord.objects.create(
                    student=student,
                    total_fee=student.course.fees,
                    paid_amount=0,
                    status='pending'
                )

            # If created from an enquiry, update the enquiry status to admitted
            from_enquiry_id = request.POST.get('from_enquiry')
            if from_enquiry_id:
                try:
                    from enquiries.models import AdmissionEnquiry
                    AdmissionEnquiry.objects.filter(pk=from_enquiry_id).update(status='admitted')
                except Exception:
                    pass

            messages.success(request, f"Student {student.full_name} ({student.student_id}) enrolled successfully! Login username: {username}")
            return redirect('students:detail', pk=student.pk)
    else:
        # Generate next student ID suggestion
        last_student = Student.objects.order_by('-id').first()
        next_num = (last_student.id + 1) if last_student else 1
        initial_id = f"NS-STU-{next_num:03d}"
        initial_data = {'student_id': initial_id, 'is_active': True, 'board': 'CBSE'}
        enquiry_obj = None

        enquiry_id = request.GET.get('enquiry')
        if enquiry_id:
            try:
                from enquiries.models import AdmissionEnquiry
                enquiry_obj = AdmissionEnquiry.objects.get(pk=enquiry_id)

                # Split student name into first and last name
                names = enquiry_obj.student_name.strip().split(maxsplit=1)
                first_name = names[0] if names else ''
                last_name = names[1] if len(names) > 1 else ''

                initial_data.update({
                    'first_name': first_name,
                    'last_name': last_name,
                    'father_name': enquiry_obj.parent_name,
                    'phone': enquiry_obj.phone,
                    'parent_phone': enquiry_obj.phone,
                    'email': enquiry_obj.email or '',
                    'board': enquiry_obj.board or 'CBSE',
                    'class_level': enquiry_obj.class_level or '',
                })

                # Try matching course by interested_course or class_level
                if enquiry_obj.interested_course:
                    matching_course = Course.objects.filter(
                        Q(name__icontains=enquiry_obj.interested_course) |
                        Q(class_level=enquiry_obj.class_level)
                    ).first()
                    if matching_course:
                        initial_data['course'] = matching_course.pk
                elif enquiry_obj.class_level:
                    matching_course = Course.objects.filter(class_level=enquiry_obj.class_level).first()
                    if matching_course:
                        initial_data['course'] = matching_course.pk
            except Exception:
                pass

        form = StudentForm(initial=initial_data)

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add New Student',
        'enquiry_obj': enquiry_obj
    })

@login_required
def student_update(request, pk):
    """Admin updates existing student details."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            # Update user info
            user = student.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            user.save()

            form.save()
            messages.success(request, f"Student {student.full_name} updated successfully!")
            return redirect('students:detail', pk=student.pk)
    else:
        initial_data = {
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
            'email': student.user.email,
            'username': student.user.username,
        }
        form = StudentForm(instance=student, initial=initial_data)

    return render(request, 'students/student_form.html', {'form': form, 'title': f'Edit Student: {student.full_name}', 'is_edit': True, 'student': student})

@login_required
def student_delete(request, pk):
    """Admin deletes a student and associated user account."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, f"Student {name} deleted successfully.")
        return redirect('students:list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})
