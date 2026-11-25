import uuid
import decimal
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from .models import FeeRecord
from .forms import FeeRecordForm
from students.models import Student

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

@login_required
def fee_list(request):
    """Admin view of all student fee records with payment status and details."""
    if not is_admin(request.user):
        if hasattr(request.user, 'student_profile'):
            return redirect('dashboard:student_dashboard')
        messages.error(request, "Permission denied.")
        return redirect('dashboard:home')

    records = FeeRecord.objects.select_related('student__user', 'student__course', 'student__batch').all()

    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    if status_filter:
        records = records.filter(status=status_filter)
    if search_query:
        records = records.filter(
            Q(student__user__first_name__icontains=search_query) |
            Q(student__user__last_name__icontains=search_query) |
            Q(student__student_id__icontains=search_query) |
            Q(receipt_number__icontains=search_query)
        )

    # Aggregates
    totals = FeeRecord.objects.aggregate(
        total_fees=Sum('total_fee'),
        total_collected=Sum('paid_amount')
    )
    total_fees = totals['total_fees'] or Decimal('0.00')
    total_collected = totals['total_collected'] or Decimal('0.00')
    total_pending = total_fees - total_collected

    context = {
        'records': records,
        'selected_status': status_filter,
        'search_query': search_query,
        'total_fees': total_fees,
        'total_collected': total_collected,
        'total_pending': total_pending,
    }
    return render(request, 'fees/fee_list.html', context)

@login_required
def fee_create(request):
    """Admin creates a new fee record."""
    if not is_admin(request.user):
        messages.error(request, "Permission denied.")
        return redirect('fees:list')

    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, f"Fee record created for {record.student.full_name}!")
            return redirect('fees:receipt', pk=record.pk)
    else:
        student_id = request.GET.get('student')
        initial_data = {'payment_date': timezone.now().date(), 'paid_amount': Decimal('0.00')}
        if student_id:
            student = get_object_or_404(Student, pk=student_id)
            initial_data['student'] = student
            if student.course:
                initial_data['total_fee'] = student.course.fees
        form = FeeRecordForm(initial=initial_data)

    return render(request, 'fees/fee_form.html', {'form': form, 'title': 'Create Fee Record'})

@login_required
def record_payment(request, pk):
    """
    Student online fee payment flow.
    Superuser / Admin cannot pay student fees.
    Only the student who owns this fee record can pay.
    """
    record = get_object_or_404(FeeRecord.objects.select_related('student__user', 'student__course', 'student__batch'), pk=pk)

    # Superuser / Admin is strictly prohibited from paying student fees
    if is_admin(request.user):
        messages.warning(request, "Administrator fee payment is disabled. Fees must be paid directly by students via their Student Portal.")
        return redirect('fees:list')

    # Student must own this fee record
    if hasattr(request.user, 'student_profile'):
        if request.user.student_profile != record.student:
            messages.error(request, "Access denied. You can only view and pay your own fees.")
            return redirect('dashboard:student_dashboard')
    else:
        messages.error(request, "Access restricted to enrolled students.")
        return redirect('dashboard:home')

    # If already fully paid
    if record.remaining_amount <= 0 or record.status == 'paid':
        messages.info(request, "This fee record has already been fully paid.")
        return redirect('fees:receipt', pk=record.pk)

    if request.method == 'POST':
        try:
            amt_str = request.POST.get('amount', '').strip()
            amt = Decimal(amt_str)
        except (ValueError, TypeError, decimal.InvalidOperation):
            amt = Decimal('0')

        if amt <= Decimal('0'):
            messages.error(request, "Please enter a valid payment amount greater than ₹0.")
            return redirect('fees:pay', pk=record.pk)

        if amt > record.remaining_amount:
            messages.error(request, f"Payment amount (₹{amt}) cannot exceed remaining balance of ₹{record.remaining_amount}.")
            return redirect('fees:pay', pk=record.pk)

        payment_method = request.POST.get('payment_method', 'upi')
        upi_id = request.POST.get('upi_id', '').strip()
        card_number = request.POST.get('card_number', '').replace(' ', '')
        bank_name = request.POST.get('bank_name', '').strip()

        txn_id = f"NS-TXN-{uuid.uuid4().hex[:8].upper()}"

        details = []
        if payment_method == 'upi':
            details.append(f"UPI ID: {upi_id}" if upi_id else "UPI QR Scan")
        elif payment_method in ['online', 'card']:
            last4 = card_number[-4:] if len(card_number) >= 4 else "Card"
            details.append(f"Card ending {last4}")
            payment_method = 'online'
        elif payment_method == 'bank':
            details.append(f"Bank: {bank_name}" if bank_name else "Net Banking")
        else:
            payment_method = 'online'

        detail_str = f" ({', '.join(details)})" if details else ""
        txn_log = f"[{timezone.now().strftime('%d %b %Y, %I:%M %p')}] Paid ₹{amt} via {payment_method.upper()}{detail_str} | Txn ID: {txn_id}"

        record.paid_amount += amt
        record.payment_date = timezone.now().date()
        record.payment_method = payment_method
        if record.remarks:
            record.remarks = f"{record.remarks}\n{txn_log}".strip()
        else:
            record.remarks = txn_log

        record.save()
        messages.success(request, f"Payment of ₹{amt} completed successfully! Transaction ID: {txn_id}. Fee receipt generated.")
        return redirect('fees:receipt', pk=record.pk)

    context = {
        'record': record,
        'remaining_amount': record.remaining_amount,
    }
    return render(request, 'fees/student_payment.html', context)

@login_required
def fee_receipt(request, pk):
    """View / Print professional fee receipt."""
    record = get_object_or_404(FeeRecord.objects.select_related('student__user', 'student__course', 'student__batch'), pk=pk)

    # Students can view their own receipt
    if hasattr(request.user, 'student_profile') and not is_admin(request.user):
        if request.user.student_profile != record.student:
            messages.error(request, "Permission denied.")
            return redirect('dashboard:student_dashboard')

    return render(request, 'fees/receipt.html', {'record': record})
