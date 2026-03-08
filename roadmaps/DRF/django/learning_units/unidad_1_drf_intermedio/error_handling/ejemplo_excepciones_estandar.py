# Ejemplo: Excepciones Estándar de DRF

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
    AuthenticationFailed,
    MethodNotAllowed,
    Throttled,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# -------------------------------------------------
# Ejemplo de View con excepciones estándar
# -------------------------------------------------
class TicketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        GET /tickets/{pk}/
        """
        # NotFound: Recurso no encontrado
        from ticket.models import Ticket
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound(f"Ticket con id {pk} no encontrado.")

        # PermissionDenied: Sin permisos
        if ticket.created_by != request.user and not request.user.is_staff:
            raise PermissionDenied("No tienes permiso para ver este ticket.")

        # Serializar y devolver
        from ticket.serializers import TicketSerializer
        return Response(TicketSerializer(ticket).data)

    def delete(self, request, pk):
        """
        DELETE /tickets/{pk}/
        """
        from ticket.models import Ticket
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound(f"Ticket con id {pk} no encontrado.")

        # PermissionDenied: Solo el creador o admin puede eliminar
        if ticket.created_by != request.user and not request.user.is_staff:
            raise PermissionDenied("No tienes permiso para eliminar este ticket.")

        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------
# Ejemplo: AuthenticationFailed
# -------------------------------------------------
class SecureDataView(APIView):
    def get(self, request):
        # AuthenticationFailed: Falló la autenticación
        # (DRF ya lo maneja automáticamente si no estás autenticado
        # en vistas con permission_classes = [IsAuthenticated])
        pass


# -------------------------------------------------
# Ejemplo: MethodNotAllowed
# -------------------------------------------------
class ReadOnlyTicketView(APIView):
    def get(self, request):
        return Response({"message": "Solo lectura"})

    def post(self, request):
        # MethodNotAllowed: Método no permitido
        raise MethodNotAllowed("POST no permitido en este endpoint.")


# -------------------------------------------------
# Ejemplo: Throttled (rate limiting)
# -------------------------------------------------
from rest_framework.throttling import UserRateThrottle


class BurstThrottleThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '10/minute'


class TicketSearchView(APIView):
    throttle_classes = [BurstThrottleThrottle]

    def get(self, request):
        # Si el usuario excede el rate, DRF lanza Throttled automáticamente
        # Pero también puedes lanzarlo manualmente:
        # raise Throttled()
        return Response({"results": []})


# -------------------------------------------------
# Tabla de referencia:
# -------------------------------------------------
"""
| Excepción              | Código | Cuándo usarla                    |
|------------------------|--------|----------------------------------|
| NotFound               | 404    | Recurso no existe               |
| PermissionDenied       | 403    | Usuario no tiene permisos       |
| AuthenticationFailed   | 401    | Credenciales inválidas          |
| MethodNotAllowed       | 405    | Método HTTP no soportado        |
| Throttled              | 429    | Rate limit excedido              |
| ValidationError        | 400    | Datos inválidos (en serializers)|
"""


# -------------------------------------------------
# Para integrar en el proyecto:
# -------------------------------------------------
# Copia las excepciones a src/ticket/views.py donde necesites
# validar objetos, permisos, etc.
