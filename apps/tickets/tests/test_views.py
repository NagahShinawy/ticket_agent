from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from apps.tickets.models import Ticket, StatusChoices


User = get_user_model()

class TicketAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

        # Create an agent user
        self.agent = User.objects.create_user(
            username='agent',
            email='agent@example.com',
            password='agentpassword'
        )

        # Create some tickets
        self.ticket1 = Ticket.objects.create(
            title='Ticket 1',
            description='Description for Ticket 1',
            status=StatusChoices.OPEN,
        )
        self.ticket2 = Ticket.objects.create(
            title='Ticket 2',
            description='Description for Ticket 2',
            status=StatusChoices.OPEN,
        )

        # Authenticate the admin and agent
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin)

        self.agent_client = APIClient()
        self.agent_client.force_authenticate(user=self.agent)

    # Test Admin Endpoints
    def test_admin_can_create_ticket(self):
        url = reverse('admin-tickets-list')
        data = {
            'title': 'New Ticket',
            'description': 'Description for New Ticket',
            'status': StatusChoices.OPEN,
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 3)

    def test_admin_can_update_ticket(self):
        url = reverse('admin-tickets-detail', args=[self.ticket1.id])
        data = {
            'title': 'Updated Ticket 1',
            'description': 'Updated Description for Ticket 1',
            'status': StatusChoices.ASSIGNED,
        }
        response = self.admin_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.title, 'Updated Ticket 1')

    def test_admin_can_delete_ticket(self):
        url = reverse('admin-tickets-detail', args=[self.ticket1.id])
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ticket.objects.count(), 1)

    # Test Agent Endpoints
    def test_agent_can_fetch_tickets(self):
        url = reverse('agent-tickets')
        response = self.agent_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming pagination is applied

    def test_agent_cannot_create_ticket(self):
        url = reverse('admin-tickets-list')
        data = {
            'title': 'New Ticket',
            'description': 'Description for New Ticket',
            'status': StatusChoices.OPEN,
        }
        response = self.agent_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_agent_cannot_update_ticket(self):
        url = reverse('admin-tickets-detail', args=[self.ticket1.id])
        data = {
            'title': 'Updated Ticket 1',
            'description': 'Updated Description for Ticket 1',
            'status': StatusChoices.ASSIGNED,
        }
        response = self.agent_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_agent_cannot_delete_ticket(self):
        url = reverse('admin-tickets-detail', args=[self.ticket1.id])
        response = self.agent_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test Pagination
    def test_pagination(self):
        url = reverse('agent-tickets')
        response = self.agent_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    # Test Authentication
    def test_unauthenticated_access(self):
        client = APIClient()
        url = reverse('agent-tickets')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)