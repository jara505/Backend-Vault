# Demostración: Serializers Avanzados en DRF
# Aplicado al proyecto de tickets
# Objetivo: Usar fields read-only/write-only, validaciones cross-field y SerializerMethodField

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
# En producción: from ticket.models import Ticket


class TicketSerializerAvanzadoDemo(ModelSerializer):
    """
    Demo de serializers avanzados aplicado a Ticket.
    En producción, reemplaza/extiende src/ticket/serializers/ticket_serializer.py.
    """

    # SerializerMethodField: Campo calculado (ej. username del creador)
    creator_username = SerializerMethodField(read_only=True)

    class Meta:
        # model = Ticket  # En producción
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "creator_username",
        ]
        read_only_fields = ["id", "created_at", "creator_username"]  # Solo lectura
        extra_kwargs = {
            "description": {
                "write_only": True
            },  # Solo escritura (no en respuesta JSON)
        }

    def get_creator_username(self, obj):
        """SerializerMethodField: Devuelve username del creador."""
        return obj.created_by.username if obj.created_by else None

    def validate(self, attrs):
        """Validación cross-field: Ejemplo - no permitir priority alta sin status open."""
        if attrs.get("priority", 3) < 3 and attrs.get("status") != "open":
            raise ValidationError("Prioridad alta solo para tickets abiertos.")
        return attrs


# Cómo probar:
# 1. Agrega a src/ticket/serializers/ticket_serializer.py o crea uno nuevo.
# 2. Usa en views: serializer_class = TicketSerializerAvanzadoDemo
# 3. POST a /api/tickets/create/: description aparece en request, pero no en respuesta (write_only).
# 4. GET: creator_username calculado aparece (read_only).
# 5. Prueba validación: POST con priority=1 y status=closed -> error.

# Ventajas:
# - Seguridad: Campos sensibles write-only.
# - Flexibilidad: Campos calculados con SerializerMethodField.
# - Validaciones: Cross-field evitan lógica inconsistente.

