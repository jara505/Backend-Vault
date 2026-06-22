# src/ticket/error_handling/validation_error.py

from rest_framework import serializers
from ..choices import TicketStatus


class TicketSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    priority = serializers.IntegerField(min_value=1, max_value=5)
    status = serializers.ChoiceField(choices=TicketStatus.choices)

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título del ticket debe tener al menos 5 caracteres."
            )
        return value

    def validate(self, attrs):
        """Validación cross-field: prioridad alta solo en tickets abiertos."""
        priority = attrs.get("priority", 3)
        status = attrs.get("status")

        if priority <= 2 and status == TicketStatus.CLOSED:
            raise serializers.ValidationError(
                "No se puede cerrar un ticket con prioridad alta (1-2)."
            )
        return attrs
