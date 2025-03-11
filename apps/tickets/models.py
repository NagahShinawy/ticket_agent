from django.db import models
from django.contrib.auth import get_user_model
from .choices import StatusChoices
from .managers import TicketManager
from apps.core.db.mixins import TimestampedModelMixin


User = get_user_model()

class Ticket(TimestampedModelMixin, models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    objects = TicketManager()

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.pk}, title={self.title}, status={self.status})"