from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TimetableEntry
from .forms import TimetableEntryForm
from batches.models import Batch

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

def is_staff_or_teacher(user):
    return is_admin(user) or (hasattr(user, 'profile') and user.profile.role == 'teacher')

@login_required
def timetable_index(request):
    """View timetable by batch."""
    batches = Batch.objects.filter(status='active').order_by('board', 'class_level', 'name')
    selected_batch_id = request.GET.get('batch')
    
    selected_batch = None
    if selected_batch_id:
        selected_batch = get_object_or_404(Batch, pk=selected_batch_id)
    elif batches.exists():
        selected_batch = batches.first()

    entries_by_day = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': [],
    }

    if selected_batch:
        entries = TimetableEntry.objects.filter(batch=selected_batch).select_related('subject', 'teacher__user').order_by('start_time')
        for entry in entries:
            if entry.day in entries_by_day:
                entries_by_day[entry.day].append(entry)

    return render(request, 'timetable/timetable_view.html', {
        'batches': batches,
        'selected_batch': selected_batch,
        'entries_by_day': entries_by_day,
        'is_admin': is_admin(request.user),
    })

@login_required
def timetable_create(request):
    """Admin creates a new timetable slot."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('timetable:index')

    batch_id = request.GET.get('batch')
    initial_data = {}
    if batch_id:
        initial_data['batch'] = batch_id

    if request.method == 'POST':
        form = TimetableEntryForm(request.POST)
        if form.is_valid():
            entry = form.save()
            messages.success(request, f"Class scheduled for {entry.batch.name} on {entry.day} ({entry.start_time}-{entry.end_time})!")
            return redirect(f"/timetable/?batch={entry.batch.id}")
    else:
        form = TimetableEntryForm(initial=initial_data)

    return render(request, 'timetable/timetable_form.html', {'form': form, 'title': 'Schedule New Class'})

@login_required
def timetable_update(request, pk):
    """Admin edits an existing timetable slot."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('timetable:index')

    entry = get_object_or_404(TimetableEntry, pk=pk)
    if request.method == 'POST':
        form = TimetableEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            messages.success(request, "Timetable slot updated successfully!")
            return redirect(f"/timetable/?batch={entry.batch.id}")
    else:
        form = TimetableEntryForm(instance=entry)

    return render(request, 'timetable/timetable_form.html', {'form': form, 'title': 'Edit Timetable Slot', 'is_edit': True, 'entry': entry})

@login_required
def timetable_delete(request, pk):
    """Admin deletes a timetable slot."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('timetable:index')

    entry = get_object_or_404(TimetableEntry, pk=pk)
    batch_id = entry.batch.id
    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Timetable slot removed successfully.")
        return redirect(f"/timetable/?batch={batch_id}")
    return render(request, 'timetable/timetable_confirm_delete.html', {'entry': entry})
