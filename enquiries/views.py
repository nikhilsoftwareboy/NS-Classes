from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AdmissionEnquiry, ContactMessage

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

@login_required
def enquiry_list(request):
    """Admin view of all admission enquiries."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    enquiries = AdmissionEnquiry.objects.all()
    status_filter = request.GET.get('status', '')
    board_filter = request.GET.get('board', '')

    if status_filter:
        enquiries = enquiries.filter(status=status_filter)
    if board_filter:
        enquiries = enquiries.filter(board=board_filter)

    counts = {
        'total': AdmissionEnquiry.objects.count(),
        'new': AdmissionEnquiry.objects.filter(status='new').count(),
        'contacted': AdmissionEnquiry.objects.filter(status='contacted').count(),
        'interested': AdmissionEnquiry.objects.filter(status='interested').count(),
        'admitted': AdmissionEnquiry.objects.filter(status='admitted').count(),
    }

    context = {
        'enquiries': enquiries,
        'counts': counts,
        'selected_status': status_filter,
        'selected_board': board_filter,
    }
    return render(request, 'enquiries/enquiry_list.html', context)

@login_required
def enquiry_update_status(request, pk):
    """Quick update of an enquiry status."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    enquiry = get_object_or_404(AdmissionEnquiry, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(AdmissionEnquiry.STATUS_CHOICES):
            enquiry.status = new_status
            enquiry.save()
            messages.success(request, f"Status updated to '{enquiry.get_status_display()}' for {enquiry.student_name}.")

    return redirect('enquiries:list')

@login_required
def enquiry_delete(request, pk):
    """Delete an admission enquiry."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    enquiry = get_object_or_404(AdmissionEnquiry, pk=pk)
    if request.method == 'POST':
        student_name = enquiry.student_name
        enquiry.delete()
        messages.success(request, f"Admission enquiry for '{student_name}' has been deleted successfully.")
    return redirect('enquiries:list')

@login_required
def contact_messages_list(request):
    """Admin view of all contact messages."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    contact_msgs = ContactMessage.objects.all()
    return render(request, 'enquiries/contact_messages.html', {'contact_msgs': contact_msgs})

@login_required
def toggle_message_read(request, pk):
    """Toggle read status for contact message."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    status_label = "read" if msg.is_read else "unread"
    messages.success(request, f"Message marked as {status_label}.")
    return redirect('enquiries:messages')

@login_required
def contact_message_delete(request, pk):
    """Delete a contact message."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        name = msg.name
        msg.delete()
        messages.success(request, f"Message from '{name}' has been deleted successfully.")
    return redirect('enquiries:messages')
