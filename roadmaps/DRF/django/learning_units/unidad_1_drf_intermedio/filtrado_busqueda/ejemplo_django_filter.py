# Demostración: Filtrado con django-filter
# Aplicado al proyecto de tickets
# Objetivo: Agregar filtros avanzados a vistas (ej. por status, priority)

# Instala: pip install django-filter (ya en requirements.txt)
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    CharFilter,
    NumberFilter,
)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# En producción: from ticket.models import Ticket
# from ticket.serializers.ticket_serializer import TicketSerializer


class TicketFilter(FilterSet):
    """
    Define filtros custom para Ticket.
    - status: filtro exacto
    - priority_min: filtro numérico (>=)
    - title_contains: búsqueda parcial en title
    """

    priority_min = NumberFilter(
        field_name="priority", lookup_expr="gte"
    )  # >= priority_min
    title_contains = CharFilter(
        field_name="title", lookup_expr="icontains"
    )  # Contiene (case-insensitive)

    class Meta:
        # model = Ticket
        fields = ["status", "priority", "priority_min", "title_contains"]


class TicketListViewConFiltroDemo(generics.ListAPIView):
    """
    Demo de django-filter en vista.
    En producción, reemplaza/extiende src/ticket/views.py -> TicketListView.
    """

    # serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter  # Usa el FilterSet custom

    def get_queryset(self):
        # Base: tickets del user (como antes)
        return Ticket.objects.filter(created_by=self.request.user)


# Cómo probar:
# 1. Agrega 'django_filters' a INSTALLED_APPS en src/core/settings.py.
# 2. Instala: pip install -r requirements/requirements.txt
# 3. Reemplaza en src/ticket/views.py: class TicketListView(TicketListViewConFiltroDemo):
# 4. Corre: python src/manage.py runserver
# 5. GET /api/tickets/?status=open&priority_min=2&title_contains=bug
#    -> Filtra tickets abiertos, priority >=2, title con "bug".

# Ventajas:
# - Fácil: Declarativo, auto-genera query params.
# - Seguro: Filtra en DB.
# - Extensible: Agrega más filtros en FilterSet.

