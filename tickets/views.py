from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Ticket

# DASHBOARD
@login_required
def dashboard(request):
    user = request.user
    if user.is_staff:
        tickets = Ticket.objects.all()[:5]
        all_tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=user)[:5]
        all_tickets = tickets

    total = all_tickets.count()
    resolved = all_tickets.filter(status='resolved').count()
    in_progress = all_tickets.filter(status='in_progress').count()
    open_tickets = all_tickets.filter(status='open').count()

    resolved_pct = int((resolved / total * 100)) if total else 0
    in_progress_pct = int((in_progress / total * 100)) if total else 0
    open_pct = 100 - resolved_pct - in_progress_pct

    return render(request, 'tickets/dashboard.html', {
        'tickets': tickets,
        'stats': {
            'total': total,
            'resolved_pct': resolved_pct,
            'in_progress_pct': in_progress_pct,
            'open_pct': open_pct,
        },
        'is_admin': user.is_staff
    })

# CREATE
@login_required
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        prio = request.POST.get('priority', 'medium')
        if title and desc:
            ticket = Ticket.objects.create(
                title=title,
                description=desc,
                priority=prio,
                created_by=request.user
            )
            messages.success(request, f"✅ Ticket {ticket.id} créé avec succès !")
            return redirect('dashboard')
        messages.error(request, "❌ Veuillez remplir tous les champs.")
    return render(request, 'tickets/create_ticket.html')

# MY TICKETS
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})

# DETAIL
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff and ticket.created_by != request.user:
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'is_admin': request.user.is_staff
    })

# EDIT (staff only)
@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce ticket.")
        return redirect('ticket_detail', ticket_id=ticket.id)

    if request.method == 'POST':
        ticket.title = request.POST.get('title')
        ticket.description = request.POST.get('description')
        ticket.status = request.POST.get('status')
        ticket.priority = request.POST.get('priority')
        ticket.save()
        messages.success(request, f"✅ Ticket {ticket.id} mis à jour.")
        return redirect('ticket_detail', ticket_id=ticket.id)

    return render(request, 'tickets/edit_ticket.html', {'ticket': ticket})

# PDF EXPORT
@login_required
def export_ticket_pdf(request, ticket_id):
    from weasyprint import HTML
    from django.utils import timezone

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff and ticket.created_by != request.user:
        return redirect('dashboard')

    html_string = render_to_string('tickets/ticket_pdf.html', {'ticket': ticket, 'user': request.user})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}_{timezone.now().strftime("%Y%m%d")}.pdf"'
    return response