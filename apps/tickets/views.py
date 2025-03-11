import logging
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
from .pagination import TicketPagination


logger = logging.getLogger(__name__)



class TicketAdminViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]
    pagination_class = TicketPagination



class AgentTicketView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = TicketPagination

    def get(self, request):
        agent = request.user
        logger.info(f"Fetching tickets for agent: {agent.username}")


        # Fetch already assigned tickets
        assigned_tickets = list(
            Ticket.objects.filter(assigned_to=agent, status=StatusChoices.ASSIGNED)[:MAX_TICKETS_PER_AGENT]
        )
        remaining_slots = MAX_TICKETS_PER_AGENT - len(assigned_tickets)

        if remaining_slots > 0:
            with transaction.atomic():
                logger.debug(f"Assigning {remaining_slots} new tickets to agent: {agent.username}")
                # Fetch and lock unassigned tickets
                unassigned_tickets = list(
                    Ticket.objects.select_for_update()
                    .filter(status=StatusChoices.OPEN)
                    .order_by('created_at')[:remaining_slots]
                )
                logger.info(f"Assigned {len(unassigned_tickets)} tickets to agent: {agent.username}")
                # Bulk update unassigned tickets
                if unassigned_tickets:
                    ticket_ids = [ticket.id for ticket in unassigned_tickets]
                    Ticket.objects.filter(id__in=ticket_ids).update(
                        assigned_to=agent, status=StatusChoices.ASSIGNED
                    )

                    # Refresh the unassigned tickets with updated data
                    unassigned_tickets = Ticket.objects.filter(id__in=ticket_ids)
                    assigned_tickets += unassigned_tickets

        paginator = self.pagination_class()
        paginated_tickets = paginator.paginate_queryset(assigned_tickets, request)


        if paginated_tickets is not None:
            serializer = TicketSerializer(paginated_tickets, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = TicketSerializer(assigned_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)