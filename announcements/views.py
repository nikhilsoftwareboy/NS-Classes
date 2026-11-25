from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Announcement
from .forms import AnnouncementForm

def is_staff_or_teacher(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['admin', 'teacher'])

@login_required
def announcement_list(request):
    """List announcements relevant to the logged-in user."""
    user = request.user
    announcements = Announcement.objects.select_related('batch', 'created_by').filter(is_active=True)

    student = getattr(user, 'student_profile', None)
    teacher = getattr(user, 'teacher_profile', None)

    if student and not is_staff_or_teacher(user):
        if student.batch:
            announcements = announcements.filter(Q(target_audience='all') | Q(target_audience='batch', batch=student.batch))
        else:
            announcements = announcements.filter(target_audience='all')
    elif teacher and not user.is_superuser and user.profile.role != 'admin':
        announcements = announcements.filter(Q(target_audience='all') | Q(target_audience='teachers') | Q(created_by=user))

    can_create = is_staff_or_teacher(user)
    return render(request, 'announcements/announcement_list.html', {
        'announcements': announcements,
        'can_create': can_create,
    })

@login_required
def announcement_create(request):
    """Admin or teacher creates an announcement."""
    if not is_staff_or_teacher(request.user):
        messages.error(request, "Permission denied.")
        return redirect('announcements:list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.created_by = request.user
            ann.save()
            messages.success(request, f"Announcement '{ann.title}' posted successfully!")
            return redirect('announcements:list')
    else:
        form = AnnouncementForm(initial={'is_active': True, 'priority': 'normal'})

    return render(request, 'announcements/announcement_form.html', {'form': form, 'title': 'Create Announcement'})

@login_required
def announcement_delete(request, pk):
    """Delete announcement."""
    if not is_staff_or_teacher(request.user):
        messages.error(request, "Permission denied.")
        return redirect('announcements:list')

    ann = get_object_or_404(Announcement, pk=pk)
    if not (request.user.is_superuser or ann.created_by == request.user or request.user.profile.role == 'admin'):
        messages.error(request, "Permission denied.")
        return redirect('announcements:list')

    if request.method == 'POST':
        title = ann.title
        ann.delete()
        messages.success(request, f"Announcement '{title}' deleted.")
        return redirect('announcements:list')
    return render(request, 'announcements/announcement_confirm_delete.html', {'announcement': ann})
