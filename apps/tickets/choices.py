from django.db import models

class StatusChoices(models.TextChoices):
    OPEN = 'open', 'Open'
    ASSIGNED = 'assigned', 'Assigned'
    CLOSED = 'closed', 'Closed'
