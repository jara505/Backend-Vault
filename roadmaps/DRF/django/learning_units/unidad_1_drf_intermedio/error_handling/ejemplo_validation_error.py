# Ejemplo: ValidationError en Serializers

from rest_framework.serializers import ModelSerializer, ValidationError


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    # -------------------------------------------------
    # 1. Validación a nivel de campo (validate_<field_name>)
    # -------------------------------------------------
    def validate_priority(self, value):
        """Valida que priority esté entre 1 y 5."""
        if value < 1 or value > 5:
            raise ValidationError("La prioridad debe estar entre 1 y 5.")
        return value

    def validate_title(self, value):
        """Valida que el título no sea demasiado corto."""
        if len(value) < 5:
            raise ValidationError("El título debe tener al menos 5 caracteres.")
        return value

    # -------------------------------------------------
    # 2. Validación cross-field (validate)
    # -------------------------------------------------
    def validate(self, attrs):
        """
        Valida relaciones entre campos.
        Ejemplo: No permitir prioridad alta si el ticket está cerrado.
        """
        priority = attrs.get('priority', 3)
        status = attrs.get('status')

        if priority < 3 and status == 'closed':
            raise ValidationError(
                "No puedes establecer prioridad alta o media en un ticket cerrado."
            )

        # Otro ejemplo: Si es urgente, debe tener descripción
        if priority == 1 and not attrs.get('description'):
            raise ValidationError(
                "Los tickets urgentes deben tener una descripción."
            )

        return attrs


# -------------------------------------------------
# Cómo probarlo:
# -------------------------------------------------
# POST /api/tickets/ con:
# {"title": "Hi", "priority": 3} -> Error: título muy corto
# {"title": "Error crítico", "priority": 1} -> Error: falta descripción
# {"title": "Error crítico", "priority": 1, "description": "..."} -> OK
# {"title": "Bug", "priority": 2, "status": "closed"} -> Error: priority media en ticket cerrado


# -------------------------------------------------
# Para integrar en el proyecto:
# -------------------------------------------------
# Copia estos métodos a src/ticket/serializers/ticket_serializer.py
