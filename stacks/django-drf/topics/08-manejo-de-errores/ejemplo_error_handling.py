# Ejemplo: Error Handling en DRF
# Aplicado al proyecto de tickets
# Objetivo: Custom exception handler, excepciones de negocio y validation errors

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import serializers


# -------------------------------------------------#
# Ejemplo 1: Custom Exception Handler
# -------------------------------------------------#

def custom_exception_handler(exc, context):
    """Normaliza todas las respuestas de error a un formato consistente."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "error": {
                "status_code": response.status_code,
                "code": getattr(exc, "default_code", "error"),
                "message": response.data.get("detail", response.data),
            }
        }

    return response

# Registrar en settings.py:
# REST_FRAMEWORK = {
#     "EXCEPTION_HANDLER": "ticket.error_handling.custom_exception_handler.custom_exception_handler",
# }


# -------------------------------------------------#
# Ejemplo 2: Excepción Custom de Negocio
# -------------------------------------------------#

class TicketBusinessRuleViolation(APIException):
    """Regla de negocio del dominio de tickets violada."""
    status_code = 422
    default_detail = "Regla de negocio de ticket violada."
    default_code = "ticket_business_rule_violation"

# Uso en una vista:
# from ticket.choices import TicketStatus
#
# class TicketUpdateView(generics.UpdateAPIView):
#     def perform_update(self, serializer):
#         ticket = self.get_object()
#         if ticket.status == TicketStatus.CLOSED:
#             raise TicketBusinessRuleViolation(
#                 "No se puede modificar un ticket cerrado."
#             )
#         serializer.save()


# -------------------------------------------------#
# Ejemplo 3: ValidationError por campo
# -------------------------------------------------#

class TicketValidationDemo(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    priority = serializers.IntegerField(min_value=1, max_value=5)

    def validate_title(self, value):
        """Validación de campo individual."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título del ticket debe tener al menos 5 caracteres."
            )
        return value


# -------------------------------------------------#
# Ejemplo 4: ValidationError cross-field
# -------------------------------------------------#

class TicketCrossFieldDemo(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    priority = serializers.IntegerField(min_value=1, max_value=5)
    status = serializers.ChoiceField(
        choices=[("open", "Open"), ("closed", "Closed")]
    )

    def validate(self, attrs):
        """No se puede cerrar un ticket con prioridad alta."""
        if attrs.get("priority", 3) <= 2 and attrs.get("status") == "closed":
            raise serializers.ValidationError(
                "No se puede cerrar un ticket con prioridad alta (1-2)."
            )
        return attrs


# Cómo probar:
# 1. Registra el handler en settings.py (ver Ejemplo 1).
# 2. Accede a un endpoint sin autenticación -> error normalizado con status_code, code, message.
# 3. En una vista de update, intenta modificar un ticket cerrado -> 422 con TicketBusinessRuleViolation.
# 4. POST a /api/tickets/create/ con title="" -> 400 con ValidationError de campo.
# 5. POST con priority=1 y status=closed -> 400 con ValidationError cross-field.

# Ventajas:
# - Consistencia: Todas las respuestas de error tienen el mismo formato JSON.
# - Separación: Validación de datos (serializer) vs reglas de negocio (custom exception).
# - Claridad: El frontend puede parsear errores de forma uniforme.
