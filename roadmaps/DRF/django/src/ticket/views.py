from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .pagination.pagination import TicketPagination
from .serializers.ticket_serializer import TicketSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .choices import TicketStatus
from .idempotency_mixin import IdempotentCreateMixin
from .filters.filters_ticket import TicketFilter
# Create your views here.


class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketPagination

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)


# probar la idenmpotencia
class TicketCreateView(IdempotentCreateMixin, generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TicketFilterActivate(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(
            status=TicketStatus.OPEN, assigned_to=self.request.user
        )


class TicketFilterSetView(generics.ListAPIView):
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)
