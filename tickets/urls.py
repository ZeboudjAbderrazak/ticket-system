from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ticket/new/', views.create_ticket, name='create_ticket'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<str:ticket_id>/edit/', views.update_ticket, name='edit_ticket'),
    path('ticket/<str:ticket_id>/pdf/', views.export_ticket_pdf, name='export_ticket_pdf'),
]