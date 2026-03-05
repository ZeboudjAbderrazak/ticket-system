from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Bas'),
        ('medium', 'Moyen'),
        ('high', 'Urgent'),
    ]

    id = models.CharField(max_length=12, primary_key=True, editable=False)
    title = models.CharField('Objet', max_length=200)
    description = models.TextField('Description')
    status = models.CharField('Statut', max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField('Priorité', max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        if not self.id:
            last = Ticket.objects.order_by('-id').first()
            num = int(last.id.split('-')[1]) + 1 if last else 1
            self.id = f"TKT-{num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.title}"