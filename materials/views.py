from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import StudyMaterial
from .forms import StudyMaterialForm
from courses.models import Subject
from batches.models import Batch

def is_teacher_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['admin', 'teacher'])

@login_required
def material_list(request):
    """List study materials filtered by role."""
    user = request.user
    materials = StudyMaterial.objects.select_related('subject', 'batch', 'uploaded_by').all()

    # Students see only relevant materials
    student = getattr(user, 'student_profile', None)
    if student and not is_teacher_or_admin(user):
        q_filter = Q(board=student.board, class_level=student.class_level) | Q(batch=student.batch)
        materials = materials.filter(q_filter)

    # Search & filters
    q = request.GET.get('q', '')
    mat_type = request.GET.get('type', '')
    subject_id = request.GET.get('subject', '')
    board = request.GET.get('board', '')
    class_level = request.GET.get('class', '')

    if q:
        materials = materials.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if mat_type:
        materials = materials.filter(material_type=mat_type)
    if subject_id:
        materials = materials.filter(subject_id=subject_id)
    if board:
        materials = materials.filter(board=board)
    if class_level:
        materials = materials.filter(class_level=class_level)

    subjects = Subject.objects.all()
    can_upload = is_teacher_or_admin(user)

    context = {
        'materials': materials,
        'subjects': subjects,
        'can_upload': can_upload,
        'selected_type': mat_type,
        'selected_subject': subject_id,
        'selected_board': board,
        'selected_class': class_level,
        'q': q,
    }
    return render(request, 'materials/material_list.html', context)

@login_required
def material_upload(request):
    """Teacher or admin uploads study material."""
    if not is_teacher_or_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('materials:list')

    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            mat = form.save(commit=False)
            mat.uploaded_by = request.user
            mat.save()
            messages.success(request, f"Study material '{mat.title}' uploaded successfully!")
            return redirect('materials:list')
    else:
        form = StudyMaterialForm()

    return render(request, 'materials/material_form.html', {'form': form, 'title': 'Upload Study Material'})

@login_required
def material_delete(request, pk):
    """Delete study material."""
    if not is_teacher_or_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('materials:list')

    mat = get_object_or_404(StudyMaterial, pk=pk)
    if not (request.user.is_superuser or mat.uploaded_by == request.user or request.user.profile.role == 'admin'):
        messages.error(request, "You can only delete materials you uploaded.")
        return redirect('materials:list')

    if request.method == 'POST':
        title = mat.title
        mat.delete()
        messages.success(request, f"Study material '{title}' deleted.")
        return redirect('materials:list')
    return render(request, 'materials/material_confirm_delete.html', {'material': mat})
