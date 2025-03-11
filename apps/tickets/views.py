from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from .models import Ticket
from .serializers import TicketSerializer
from .choices import StatusChoices
from .constants import MAX_TICKETS_PER_AGENT


class TicketAdminViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]



class AgentTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent = request.user

        # Fetch already assigned tickets
        assigned_tickets = list(
            Ticket.objects.filter(assigned_to=agent, status=StatusChoices.ASSIGNED)[:MAX_TICKETS_PER_AGENT]
        )
        remaining_slots = MAX_TICKETS_PER_AGENT - len(assigned_tickets)

        if remaining_slots > 0:
            with transaction.atomic():
                # Fetch and lock unassigned tickets
                unassigned_tickets = list(
                    Ticket.objects.select_for_update()
                    .filter(status=StatusChoices.OPEN)
                    .order_by('created_at')[:remaining_slots]
                )

                # Bulk update unassigned tickets
                if unassigned_tickets:
                    ticket_ids = [ticket.id for ticket in unassigned_tickets]
                    Ticket.objects.filter(id__in=ticket_ids).update(
                        assigned_to=agent, status=StatusChoices.ASSIGNED
                    )

                    # Refresh the unassigned tickets with updated data
                    unassigned_tickets = Ticket.objects.filter(id__in=ticket_ids)
                    assigned_tickets += unassigned_tickets

        serializer = TicketSerializer(assigned_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)