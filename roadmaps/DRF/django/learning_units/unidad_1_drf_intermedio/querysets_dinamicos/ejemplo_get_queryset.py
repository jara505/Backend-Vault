# Demostración: Querysets Dinámicos en Views de DRF
# Aplicado al proyecto de tickets
# Objetivo: Usar get_queryset() para filtrar dinámicamente por usuario o contexto

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# En producción: from ticket.models import Ticket
# from ticket.serializers.ticket_serializer import TicketSerializer


class TicketListViewDemo(generics.ListAPIView):
    """
    Demo de get_queryset() para filtrar tickets por usuario autenticado.
    En producción, reemplaza esto en src/ticket/views.py -> TicketListView.
    """

    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtra tickets creados por el usuario actual.
        - Usa self.request.user para contexto dinámico.
        - Evita filtrar en el template o serializer; hazlo aquí para performance.
        """
        user = self.request.user
        # Filtrado por usuario: solo tickets creados por el user logueado
        return Ticket.objects.filter(created_by=user).order_by("-created_at")


# Cómo probar:
# 1. Reemplaza en src/ticket/views.py: class TicketListView(TicketListViewDemo):
# 2. Corre: python src/manage.py runserver
# 3. Haz GET a /api/tickets/ con auth (JWT). Solo verás tus tickets.
# 4. Para más contexto: Agrega query params, ej. ?status=open para filtrar extra.

# Ventajas:
# - Seguridad: No filtras en frontend.
# - Performance: Query optimizada.
# - Reutilizable: Cambia lógica por vista (ej. admin ve todos, user solo suyos).

