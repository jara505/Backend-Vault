# src/ticket/error_handling/custom_exeptions.py

from rest_framework.exceptions import APIException


class TicketBusinessRuleViolation(APIException):
    """Regla de negocio del dominio de tickets violada."""
    status_code = 422
    default_detail = "Regla de negocio de ticket violada."
    default_code = "ticket_business_rule_violation"


# Uso en views.py o serializers:
#
# from ticket.error_handling.custom_exeptions import TicketBusinessRuleViolation
#
# if ticket.status == TicketStatus.CLOSED:
#     raise TicketBusinessRuleViolation("No se puede modificar un ticket cerrado.")
#
# if ticket.priority < 1:
#     raise TicketBusinessRuleViolation("La prioridad no puede ser menor a 1.")
#
# Protip: no crear excepciones que ya existen en DRF
# (NotFound, PermissionDenied, ValidationError, etc.)
