from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Subject
from .forms import CourseForm, SubjectForm
from batches.models import Batch

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

@login_required
def course_manage_list(request):
    """Admin courses management page."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    courses = Course.objects.prefetch_related('subjects').all()
    subjects = Subject.objects.all()
    return render(request, 'courses/course_manage_list.html', {
        'courses': courses,
        'subjects': subjects,
    })

@login_required
def course_create(request):
    """Admin creates a new course."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course '{course.name}' created successfully!")
            return redirect('courses:manage_list')
    else:
        form = CourseForm(initial={'is_active': True})

    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create New Course'})

@login_required
def course_update(request, pk):
    """Admin updates an existing course."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.name}' updated successfully!")
            return redirect('courses:manage_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/course_form.html', {'form': form, 'title': f'Edit Course: {course.name}', 'is_edit': True})

@login_required
def course_delete(request, pk):
    """Admin deletes a course."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f"Course '{name}' deleted successfully.")
        return redirect('courses:manage_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})
