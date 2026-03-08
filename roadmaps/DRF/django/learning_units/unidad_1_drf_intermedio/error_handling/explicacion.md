# Error Handling en DRF

El manejo de errores es fundamental para APIs robustas. Permite controlar qué ven los usuarios cuando algo falla y dar mensajes claros.

## ¿Por qué implementarlo?

- **Debugging:** Mensajes de error claros facilitan encontrar problemas.
- **UX:** Los clientes saben qué hacer cuando algo falla.
- **Seguridad:** Evita exponer detalles internos del servidor.
- **Consistencia:** Formato uniforme de respuestas de error.

## Tipos de Error Handling en DRF

### 1. ValidationError en Serializers

Lanza errores de validación en nivel de campo o a nivel de objeto.

```python
from rest_framework.serializers import ValidationError

class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, attrs):
        # Validación cross-field
        if attrs.get('priority', 3) < 3 and attrs.get('status') != 'open':
            raise ValidationError("Prioridad alta solo para tickets abiertos.")
        return attrs

    def validate_priority(self, value):
        # Validación a nivel de campo
        if value < 1 or value > 5:
            raise ValidationError("La prioridad debe estar entre 1 y 5.")
        return value
```

### 2. Excepciones Estándar de DRF

DRF provee excepciones built-in que puedes usar en tus views:

| Excepción | Cuándo Usarla | Código HTTP |
|-----------|---------------|-------------|
| `NotFound` | Recurso no encontrado | 404 |
| `PermissionDenied` | Sin permisos | 403 |
| `AuthenticationFailed` | Autenticación fallida | 401 |
| `MethodNotAllowed` | Método HTTP no permitido | 405 |
| `Throttled` | Rate limit excedido | 429 |

```python
from rest_framework.exceptions import NotFound, PermissionDenied, AuthenticationFailed

class TicketDetailView(APIView):
    def get(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise NotFound("Ticket no encontrado.")

        if not request.user.has_perm('ticket.view_ticket', ticket):
            raise PermissionDenied("No tienes permiso para ver este ticket.")

        return Response(TicketSerializer(ticket).data)
```

### 3. Excepciones Personalizadas

Crea excepciones propias para tu dominio de negocio.

```python
# ticket/exceptions.py
from rest_framework.exceptions import APIException

class TicketClosedException(APIException):
    status_code = 400
    default_detail = "No se puede modificar un ticket cerrado."
    default_code = "ticket_closed"

class TicketAssignmentException(APIException):
    status_code = 403
    default_detail = "No tienes permiso para asignar este ticket."
    default_code = "ticket_assignment_forbidden"
```

### 4. Custom Exception Handler Global

Estandariza el formato de todas las respuestas de error.

```python
# core/exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'success': False,
            'error': {
                'code': exc.__class__.__name__,
                'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                'status_code': response.status_code,
            }
        }

    return response
```

## Cómo integrarlo al proyecto:

### 1. ValidationError
En `src/ticket/serializers/ticket_serializer.py`, agrega validaciones:

```python
def validate(self, attrs):
    if attrs.get('priority', 3) < 3 and attrs.get('status') == 'closed':
        raise ValidationError("Prioridad alta solo para tickets abiertos.")
    return attrs
```

### 2. Excepciones Estándar
En `src/ticket/views.py`, usa las excepciones donde necesites:

```python
from rest_framework.exceptions import NotFound, PermissionDenied

def get_object(self, pk):
    try:
        return Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        raise NotFound(f"Ticket con id {pk} no encontrado.")
```

### 3. Excepciones Personalizadas
Crea `src/ticket/exceptions.py` y úsalas en views/serializers.

### 4. Custom Exception Handler
En `src/core/settings.py`, agrega:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exception_handlers.custom_exception_handler',
}
```

## Ejemplo: Respuestas de Error

### Sin Custom Handler (default DRF)
```json
{"detail": "Ticket no encontrado."}
```

### Con Custom Handler
```json
{
    "success": false,
    "error": {
        "code": "NotFound",
        "message": "Ticket no encontrado.",
        "status_code": 404
    }
}
```

## Cuándo usar cuál?

| Mecanismo | Cuándo usarlo | Status Code |
|-----------|---------------|-------------|
| `ValidationError` (serializer) | Datos del request inválidos (campos, formato, relaciones) | 400 |
| Excepciones custom de negocio | Regla de dominio violada (lógica de negocio) | 400/422 |
| Excepciones built-in de DRF | `NotFound`, `PermissionDenied`, `NotAuthenticated`, etc. | 404, 403, 401 |
| Custom Exception Handler | Normalizar el formato de **todas** las respuestas de error | — |

## Errores Comunes

- **No registrar el handler:** Sin la config en `settings.py`, tu handler custom no se usa.
- **Crear excepciones redundantes:** No dupliques `NotFound` o `PermissionDenied`, DRF ya las tiene.
- **Mezclar ValidationError con reglas de negocio:** `ValidationError` es para datos mal formados; lógica de dominio va en excepciones custom.
- **Olvidar `if response is not None`:** Si la excepción no es de DRF, el handler retorna `None` y Django lo maneja como 500.

## Mejores Prácticas

- **Usa excepciones específicas:** No muestres errores genéricos.
- **Logs:** Registra errores para debugging (sin exponer detalles al cliente).
- **Custom handler:** Estandariza el formato de errores.
- **Validaciones en serializers:** Son el primer línea de defensa.
- **No expongas stack traces:** Son para desarrollo, no producción.

## Recursos

- [DRF Exceptions](https://www.django-rest-framework.org/api-guide/exceptions/)
- [Custom Exception Handling](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling)
