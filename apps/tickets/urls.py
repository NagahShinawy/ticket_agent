from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketAdminViewSet, AgentTicketView

router = DefaultRouter()
router.register(r'admin/tickets', TicketAdminViewSet, basename='admin-tickets')

urlpatterns = [
    path('', include(router.urls)),
    path('agent/tickets/', AgentTicketView.as_view(), name='agent-tickets'),
]