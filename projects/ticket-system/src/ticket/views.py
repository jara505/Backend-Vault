from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .pagination.pagination import TicketPagination
from .serializers.ticket_serializer import TicketSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied  # Excepciones estándar (Opción 2)
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


# ============================================================
# Vistas con Excepciones Estándar (Opción 2)
# ============================================================

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar o eliminar un ticket específico.
    Implementa NotFound y PermissionDenied como ejemplo de manejo de errores.
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Solo devuelve tickets del usuario actual o si es staff
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=self.request.user)

    def get_object(self):
        """
        Override para lanzar NotFound si el ticket no existe.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        
        try:
            obj = queryset.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound(f"Ticket con id {pk} no encontrado.")
        
        return obj

    def perform_update(self, serializer):
        """
        Override para lanzar PermissionDenied si el ticket está cerrado.
        """
        ticket = self.get_object()
        
        if ticket.status == TicketStatus.CLOSED:
            raise PermissionDenied("No se puede modificar un ticket cerrado.")
        
        serializer.save()

    def perform_destroy(self, instance):
        """
        Override para lanzar PermissionDenied si no es el creador.
        """
        if instance.created_by != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("No tienes permiso para eliminar este ticket.")
        
        instance.delete()
