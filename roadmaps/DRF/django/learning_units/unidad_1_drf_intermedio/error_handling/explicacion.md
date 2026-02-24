# Error Handling en DRF: Custom Exception Handler, Excepciones de Negocio y ValidationError

El manejo de errores controla cómo tu API comunica problemas al cliente. DRF tiene un handler por defecto, pero personalizarlo te da respuestas consistentes y legibles.

## ¿Por qué personalizarlo?

- **Consistencia:** Todas las respuestas de error siguen el mismo formato JSON.
- **Debugging:** Un formato estandarizado facilita que el frontend maneje errores de forma uniforme.
- **Separación de concerns:** Las reglas de negocio lanzan excepciones propias, no se mezclan con errores HTTP genéricos.

## 1. Custom Exception Handler

DRF procesa todas las excepciones a través de un handler central. Por defecto devuelve formatos distintos según el tipo de error. Sobreescribiéndolo, normalizás todo a un formato único.

### Implementación

```python
# src/ticket/error_handling/custom_exception_handler.py
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
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
```

### Registro en settings.py

```python
# src/core/settings.py
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "ticket.error_handling.custom_exception_handler.custom_exception_handler",
}
```

### Response de ejemplo

Sin handler custom:
```json
{"detail": "No encontrado."}
```

Con handler custom:
```json
{
    "error": {
        "status_code": 404,
        "code": "not_found",
        "message": "No encontrado."
    }
}
```

## 2. Excepciones Custom de Negocio

Cuando una regla de dominio se viola (no es un error de validación de campo ni un 404), creás tu propia excepción heredando de `APIException`.

```python
# src/ticket/error_handling/custom_exeptions.py
from rest_framework.exceptions import APIException

class TicketBusinessRuleViolation(APIException):
    status_code = 422
    default_detail = "Regla de negocio de ticket violada."
    default_code = "ticket_business_rule_violation"
```

### Uso en vistas o serializers

```python
from ticket.error_handling.custom_exeptions import TicketBusinessRuleViolation
from ticket.choices import TicketStatus

# En una vista o perform_update
if ticket.status == TicketStatus.CLOSED:
    raise TicketBusinessRuleViolation("No se puede modificar un ticket cerrado.")

if ticket.priority < 1:
    raise TicketBusinessRuleViolation("La prioridad no puede ser menor a 1.")
```

### Response con el handler custom

```json
{
    "error": {
        "status_code": 422,
        "code": "ticket_business_rule_violation",
        "message": "No se puede modificar un ticket cerrado."
    }
}
```

> **Protip:** No crees excepciones para cosas que DRF ya maneja: `NotFound` (404), `PermissionDenied` (403), `ValidationError` (400), `NotAuthenticated` (401).

## 3. ValidationError en Serializers

Para errores de validación de datos (campos individuales o cross-field), usá `serializers.ValidationError` dentro del serializer. DRF los procesa automáticamente.

### Validación por campo

```python
# src/ticket/error_handling/validation_error.py
from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    priority = serializers.IntegerField(min_value=1, max_value=5)

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "El título del ticket debe tener al menos 5 caracteres."
            )
        return value
```

### Validación cross-field

```python
def validate(self, attrs):
    priority = attrs.get("priority", 3)
    status = attrs.get("status")

    if priority <= 2 and status == TicketStatus.CLOSED:
        raise serializers.ValidationError(
            "No se puede cerrar un ticket con prioridad alta (1-2)."
        )
    return attrs
```

## Cuándo usar cuál?

| Mecanismo | Cuándo usarlo | Status Code |
|-----------|---------------|-------------|
| `ValidationError` (serializer) | Datos del request inválidos (campos, formato, relaciones) | 400 |
| `TicketBusinessRuleViolation` | Regla de dominio violada (lógica de negocio) | 422 |
| Excepciones built-in de DRF | `NotFound`, `PermissionDenied`, `NotAuthenticated`, etc. | 404, 403, 401 |
| Custom Exception Handler | Normalizar el formato de **todas** las respuestas de error | — |

## Errores Comunes

- **No registrar el handler:** Sin la config en `settings.py`, tu handler custom no se usa.
- **Crear excepciones redundantes:** No dupliques `NotFound` o `PermissionDenied`, DRF ya las tiene.
- **Mezclar ValidationError con reglas de negocio:** `ValidationError` es para datos mal formados; lógica de dominio va en excepciones custom.
- **Olvidar `if response is not None`:** Si la excepción no es de DRF (ej. un `TypeError`), `exception_handler` retorna `None` y Django lo maneja como 500.

## Recursos

- [DRF Docs: Exceptions](https://www.django-rest-framework.org/api-guide/exceptions/)
- [DRF Docs: Custom Exception Handling](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling)
