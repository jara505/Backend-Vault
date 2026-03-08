# Ejemplo: Excepciones Personalizadas

from rest_framework.exceptions import APIException


# -------------------------------------------------
# 1. Excepciones del dominio de negocio (Tickets)
# -------------------------------------------------

class TicketClosedException(APIException):
    """Excepción cuando se intenta modificar un ticket cerrado."""
    status_code = 400
    default_detail = "No se puede modificar un ticket que está cerrado."
    default_code = "ticket_closed"


class TicketAlreadyAssignedException(APIException):
    """Excepción cuando el ticket ya está asignado."""
    status_code = 400
    default_detail = "Este ticket ya está asignado a otro usuario."
    default_code = "ticket_already_assigned"


class TicketAssignmentException(APIException):
    """Excepción cuando no tienes permiso para asignar."""
    status_code = 403
    default_detail = "No tienes permiso para asignar este ticket."
    default_code = "ticket_assignment_forbidden"


class TicketPriorityException(APIException):
    """Excepción para errores de prioridad."""
    status_code = 400
    default_detail = "La prioridad no es válida para este estado del ticket."
    default_code = "invalid_priority_for_status"


# -------------------------------------------------
# 2. Cómo usarlas en Serializers
# -------------------------------------------------
"""
from rest_framework.serializers import ValidationError
from .exceptions import TicketClosedException, TicketPriorityException

class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, attrs):
        ticket = self.instance
        
        # Si es una actualización de un ticket existente
        if ticket and ticket.status == 'closed':
            raise TicketClosedException()

        # Validar prioridad según estado
        priority = attrs.get('priority', 3)
        status = attrs.get('status', ticket.status if ticket else 'open')
        
        if priority < 3 and status == 'closed':
            raise TicketPriorityException()

        return attrs
"""


# -------------------------------------------------
# 3. Cómo usarlas en Views
# -------------------------------------------------
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from .exceptions import TicketClosedException, TicketAlreadyAssignedException

class TicketAssignView(APIView):
    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)

        if ticket.assigned_to:
            raise TicketAlreadyAssignedException()

        ticket.assigned_to = request.user
        ticket.save()
        
        return Response({"message": "Ticket asignado"})
"""


# -------------------------------------------------
# 4. Ejemplo con detalle custom
# -------------------------------------------------
class TicketNotEditableException(APIException):
    status_code = 403
    default_detail = "El ticket no puede ser editado."
    default_code = "ticket_not_editable"

    def __init__(self, ticket_id=None, reason=None):
        detail = self.default_detail
        if ticket_id:
            detail = f"Ticket #{ticket_id} no puede ser editado."
        if reason:
            detail += f" Razón: {reason}"
        
        self.detail = {"detail": detail, "code": self.default_code}


# -------------------------------------------------
# Uso:
# raise TicketNotEditableException(ticket_id=5, reason="Estado: cerrado")
# Respuesta:
# {
#     "detail": "Ticket #5 no puede ser editado. Razón: Estado: cerrado",
#     "code": "ticket_not_editable"
# }


# -------------------------------------------------
# Para integrar en el proyecto:
# -------------------------------------------------
# 1. Crea src/ticket/exceptions.py con estas clases
# 2. Impórtalas en serializers y views donde necesites
# 3. úsalas con raise TicketClosedException(), etc.
