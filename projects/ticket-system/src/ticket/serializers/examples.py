"""
Ejemplos de campos personalizados en DRF serializers.
Estos son fuera de la clase TicketSerializer, para practicar sin confundir el código real.
Cada caso tiene comentarios explicando cuándo usarlo y por qué.
"""

from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from ..models import Ticket


# EJEMPLO 1: CharField con source para relaciones simples (ej. acceder a un campo de un modelo relacionado)
# Caso de uso: Cuando querés mostrar un campo directo de una relación ForeignKey sin lógica extra.
# Ventajas: Simple, eficiente, no necesita método. Usá cuando no hay cálculos ni validaciones.
# Desventajas: No flexible para lógica personalizada.
class TicketSerializerExample1(ModelSerializer):
    # Accede directo al username del usuario que creó el ticket
    username = CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "title", "username"]  # Solo campos específicos, no __all__


# EJEMPLO 2: SerializerMethodField para cálculos o lógica simple
# Caso de uso: Cuando el campo requiere un cálculo básico o transformación (ej. concatenar strings, formatear fechas).
# Ventajas: Flexible, usás obj para acceder a todo el objeto.
# Desventajas: Un poco más código, pero necesario si CharField no alcanza.
class TicketSerializerExample2(ModelSerializer):
    # Calcula si el ticket está asignado (booleano basado en si assigned_to existe)
    is_assigned = SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "title", "is_assigned"]

    def get_is_assigned(self, obj):
        return obj.assigned_to is not None  # Lógica simple con obj


# EJEMPLO 3: SerializerMethodField para validaciones o lógica compleja
# Caso de uso: Cuando el campo incluye validaciones, condicionales o acceso a múltiples campos (ej. estado del ticket con reglas).
# Ventajas: Máxima flexibilidad, podés hacer casi cualquier cosa.
# Desventajas: Más código; si es reusable, movelo al modelo.
class TicketSerializerExample3(ModelSerializer):
    # Campo calculado con lógica: prioridad alta si priority < 3 y status es OPEN
    priority_status = SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "title", "priority", "status", "priority_status"]

    def get_priority_status(self, obj):
        if obj.priority < 3 and obj.status == "open":
            return "Alta prioridad - Abierto"
        return "Normal"  # Lógica condicional usando obj


# EJEMPLO 4: Combinando ambos (CharField y SerializerMethodField)
# Caso de uso: Mezclar campos directos con calculados para un serializer completo.
class TicketSerializerExample4(ModelSerializer):
    # Relación simple
    username = CharField(source="created_by.username", read_only=True)
    # Cálculo
    days_since_created = SerializerMethodField()

    class Meta:
        model = Ticket
        fields = "__all__"  # Incluye todo del modelo + estos campos personalizados

    def get_days_since_created(self, obj):
        from django.utils import timezone

        delta = timezone.now() - obj.created_at
        return delta.days  # Cálculo con fecha


# NOTA GENERAL: Siempre declara el campo en la clase (ej. username = CharField(...)) para que aparezca en el JSON.
# Si usás SerializerMethodField, define def get_<campo>(self, obj): ...
# Para relaciones, usá puntos en source (no __ como en querysets).
# Proba en la API para ver el JSON resultante.
