from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile
from .models import Teacher
from .forms import TeacherForm
from batches.models import Batch
from timetable.models import TimetableEntry

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

@login_required
def teacher_list(request):
    """Admin view of all teachers."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    teachers = Teacher.objects.select_related('user').prefetch_related('specialization').all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_detail(request, pk):
    """Teacher profile detail view."""
    teacher = get_object_or_404(Teacher.objects.select_related('user').prefetch_related('specialization'), pk=pk)
    assigned_batches = Batch.objects.filter(teacher=teacher)
    timetable_entries = TimetableEntry.objects.filter(teacher=teacher).order_by('day', 'start_time')

    context = {
        'teacher': teacher,
        'assigned_batches': assigned_batches,
        'timetable_entries': timetable_entries,
    }
    return render(request, 'teachers/teacher_detail.html', context)

@login_required
def teacher_create(request):
    """Admin creates a new teacher and User account."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data.get('username') or form.cleaned_data['teacher_id'].lower().replace('-', '_')
            password = form.cleaned_data.get('password') or 'teacher@123'

            if User.objects.filter(username=username).exists():
                messages.error(request, f"Username '{username}' already exists. Please choose a different one.")
                return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Add New Teacher'})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            UserProfile.objects.create(user=user, role='teacher', phone=form.cleaned_data.get('phone', ''))

            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()
            form.save_m2m()

            messages.success(request, f"Teacher {teacher.full_name} created successfully! Login username: {username}")
            return redirect('teachers:list')
    else:
        last_teacher = Teacher.objects.order_by('-id').first()
        next_num = (last_teacher.id + 1) if last_teacher else 1
        initial_id = f"NS-TCH-{next_num:03d}"
        form = TeacherForm(initial={'teacher_id': initial_id, 'is_active': True})

    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Add New Teacher'})

@login_required
def teacher_update(request, pk):
    """Admin updates existing teacher."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            user = teacher.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            user.save()

            form.save()
            messages.success(request, f"Teacher {teacher.full_name} updated successfully!")
            return redirect('teachers:detail', pk=teacher.pk)
    else:
        initial_data = {
            'first_name': teacher.user.first_name,
            'last_name': teacher.user.last_name,
            'email': teacher.user.email,
            'username': teacher.user.username,
        }
        form = TeacherForm(instance=teacher, initial=initial_data)

    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': f'Edit Teacher: {teacher.full_name}', 'is_edit': True, 'teacher': teacher})

@login_required
def teacher_delete(request, pk):
    """Admin deletes a teacher."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        name = teacher.full_name
        user = teacher.user
        teacher.delete()
        user.delete()
        messages.success(request, f"Teacher {name} removed successfully.")
        return redirect('teachers:list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})
