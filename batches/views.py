from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Batch
from .forms import BatchForm
from students.models import Student
from timetable.models import TimetableEntry

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

def is_teacher_or_admin(user):
    return is_admin(user) or (hasattr(user, 'profile') and user.profile.role == 'teacher')

@login_required
def batch_list(request):
    """View all batches (filtered by teacher if teacher)."""
    if not is_teacher_or_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    batches = Batch.objects.select_related('course', 'teacher__user').prefetch_related('subjects', 'students').all()
    
    board = request.GET.get('board', '')
    status = request.GET.get('status', '')
    if board:
        batches = batches.filter(board=board)
    if status:
        batches = batches.filter(status=status)

    return render(request, 'batches/batch_list.html', {
        'batches': batches,
        'selected_board': board,
        'selected_status': status,
    })

@login_required
def batch_detail(request, pk):
    """Detail view of a batch: timetable, students list, capacity."""
    batch = get_object_or_404(Batch.objects.select_related('course', 'teacher__user').prefetch_related('subjects'), pk=pk)
    students = Student.objects.filter(batch=batch).select_related('user')
    timetable_entries = TimetableEntry.objects.filter(batch=batch).select_related('subject', 'teacher__user').order_by('day', 'start_time')

    # Available unassigned students in same class/board
    available_students = Student.objects.filter(
        board=batch.board,
        class_level=batch.class_level,
        batch__isnull=True,
        is_active=True
    ).select_related('user')

    context = {
        'batch': batch,
        'students': students,
        'timetable_entries': timetable_entries,
        'available_students': available_students,
    }
    return render(request, 'batches/batch_detail.html', context)

@login_required
def batch_create(request):
    """Admin creates a new batch."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            batch = form.save()
            messages.success(request, f"Batch '{batch.name}' created successfully!")
            return redirect('batches:detail', pk=batch.pk)
    else:
        form = BatchForm(initial={'status': 'active', 'max_students': 30})

    return render(request, 'batches/batch_form.html', {'form': form, 'title': 'Create New Batch'})

@login_required
def batch_update(request, pk):
    """Admin updates existing batch."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, f"Batch '{batch.name}' updated successfully!")
            return redirect('batches:detail', pk=batch.pk)
    else:
        form = BatchForm(instance=batch)

    return render(request, 'batches/batch_form.html', {'form': form, 'title': f'Edit Batch: {batch.name}', 'is_edit': True})

@login_required
def batch_delete(request, pk):
    """Admin deletes a batch."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    batch = get_object_or_404(Batch, pk=pk)
    if request.method == 'POST':
        name = batch.name
        batch.delete()
        messages.success(request, f"Batch '{name}' deleted successfully.")
        return redirect('batches:list')
    return render(request, 'batches/batch_confirm_delete.html', {'batch': batch})

@login_required
def assign_student(request, batch_id):
    """Assign or remove student from batch."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    batch = get_object_or_404(Batch, pk=batch_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, pk=student_id)

        if action == 'assign':
            if batch.is_full:
                messages.error(request, f"Batch '{batch.name}' is already at full capacity ({batch.max_students}).")
            else:
                student.batch = batch
                student.save()
                messages.success(request, f"Student {student.full_name} assigned to {batch.name}.")
        elif action == 'remove':
            student.batch = None
            student.save()
            messages.success(request, f"Student {student.full_name} removed from batch.")

    return redirect('batches:detail', pk=batch.pk)
