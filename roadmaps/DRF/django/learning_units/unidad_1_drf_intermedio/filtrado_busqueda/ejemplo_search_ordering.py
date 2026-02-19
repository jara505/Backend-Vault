# Demostración: SearchFilter y OrderingFilter (DRF built-in)
# Aplicado al proyecto de tickets
# Objetivo: Agregar búsqueda y ordenamiento a vistas

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
# En producción: from ticket.models import Ticket
# from ticket.serializers.ticket_serializer import TicketSerializer

class TicketListViewConSearchOrderingDemo(generics.ListAPIView):
    """
    Demo de SearchFilter y OrderingFilter en vista.
    En producción, reemplaza/extiende src/ticket/views.py -> TicketListView.
    """
    # serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']  # Campos para búsqueda (icontains por defecto)
    ordering_fields = ['created_at', 'priority', 'status']  # Campos para ordenar
    ordering = ['-created_at']  # Orden por defecto (descendente)

    def get_queryset(self):
        # Base: tickets del user
        return Ticket.objects.filter(created_by=self.request.user)

# Cómo probar:
# 1. Ya incluido en DRF; no necesita instalar.
# 2. Reemplaza en src/ticket/views.py: class TicketListView(TicketListViewConSearchOrderingDemo):
# 3. Corre: python src/manage.py runserver
# 4. GET /api/tickets/?search=bug&ordering=-priority
#    -> Busca "bug" en title/description, ordena por priority descendente.
# 5. Combinable: ?search=error&ordering=created_at

# Ventajas:
# - Simple: Built-in, sin extra dependencias.
# - Flexible: search_fields para texto, ordering_fields para sorts.
# - Performance: Usa DB indexes.