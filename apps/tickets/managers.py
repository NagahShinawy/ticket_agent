from django.db import models


class TicketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()