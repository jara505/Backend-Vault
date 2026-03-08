# Ejemplo: Custom Exception Handler Global

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


# -------------------------------------------------
# 1. Custom Exception Handler Básico
# -------------------------------------------------
def custom_exception_handler(exc, context):
    """
    Manejador global de excepciones.
    Estandariza el formato de todas las respuestas de error.
    """
    # Llama al handler por defecto de DRF primero
    response = exception_handler(exc, context)

    if response is not None:
        # Estandariza el formato de respuesta
        response.data = {
            'success': False,
            'error': {
                'code': exc.__class__.__name__,
                'message': _get_error_message(exc),
                'status_code': response.status_code,
            }
        }

    return response


def _get_error_message(exc):
    """Extrae el mensaje de error de manera segura."""
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, dict):
            # ValidationError con múltiples campos
            return exc.detail
        return str(exc.detail)
    return str(exc)


# -------------------------------------------------
# 2. Custom Handler con Logging
# -------------------------------------------------
def custom_exception_handler_with_logging(exc, context):
    """
    Custom handler que también registra los errores.
    """
    # Loguea el error
    request = context.get('request')
    view = context.get('view')
    
    logger.error(
        f"Error en {view.__class__.__name__}: {exc}",
        extra={
            'request': request.path if request else None,
            'method': request.method if request else None,
            'user': request.user.username if request and request.user else 'Anonymous',
        }
    )

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'success': False,
            'error': {
                'code': exc.__class__.__name__,
                'message': _get_error_message(exc),
                'status_code': response.status_code,
                # En desarrollo, incluye más detalles
                # 'extra': str(exc) if settings.DEBUG else None,
            }
        }

    return response


# -------------------------------------------------
# 3. Custom Handler para Diferentes Tipos
# -------------------------------------------------
def custom_exception_handler_advanced(exc, context):
    """
    Handler avanzado con manejo específico por tipo de error.
    """
    response = exception_handler(exc, context)
    
    if response is None:
        # Error inesperado (500)
        return Response(
            {
                'success': False,
                'error': {
                    'code': 'InternalServerError',
                    'message': 'Error interno del servidor.',
                    'status_code': 500,
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Personaliza según el tipo de excepción
    if response.status_code == 404:
        response.data = {
            'success': False,
            'error': {
                'code': 'NotFound',
                'message': 'Recurso no encontrado.',
                'status_code': 404,
            }
        }
    elif response.status_code == 403:
        response.data = {
            'success': False,
            'error': {
                'code': 'PermissionDenied',
                'message': 'No tienes permiso para acceder a este recurso.',
                'status_code': 403,
            }
        }
    elif response.status_code == 400:
        response.data = {
            'success': False,
            'error': {
                'code': 'ValidationError',
                'message': _get_error_message(exc),
                'status_code': 400,
            }
        }
    elif response.status_code == 401:
        response.data = {
            'success': False,
            'error': {
                'code': 'AuthenticationFailed',
                'message': 'Autenticación requerida.',
                'status_code': 401,
            }
        }
    else:
        # Otros errores
        response.data = {
            'success': False,
            'error': {
                'code': exc.__class__.__name__,
                'message': _get_error_message(exc),
                'status_code': response.status_code,
            }
        }

    return response


# -------------------------------------------------
# 4. Configuración en settings.py
# -------------------------------------------------
"""
# src/core/settings.py

REST_FRAMEWORK = {
    # ... otras configuraciones ...
    
    # Handler personalizado (elige uno)
    'EXCEPTION_HANDLER': 'ruta.al.modulo.custom_exception_handler',
    
    # Por ejemplo:
    # 'EXCEPTION_HANDLER': 'core.exception_handlers.custom_exception_handler',
}
"""


# -------------------------------------------------
# Ejemplo de respuesta:
# -------------------------------------------------
"""
# Sin custom handler:
{"detail": "Ticket no encontrado."}

# Con custom handler:
{
    "success": False,
    "error": {
        "code": "NotFound",
        "message": "Ticket no encontrado.",
        "status_code": 404
    }
}

# ValidationError con custom handler:
{
    "success": False,
    "error": {
        "code": "ValidationError",
        "message": {
            "title": ["El título debe tener al menos 5 caracteres."],
            "priority": ["La prioridad debe estar entre 1 y 5."]
        },
        "status_code": 400
    }
}
"""


# -------------------------------------------------
# Para integrar en el proyecto:
# -------------------------------------------------
# 1. Crea src/core/exception_handlers.py con estas funciones
# 2. En src/core/settings.py, agrega:
#    'EXCEPTION_HANDLER': 'core.exception_handlers.custom_exception_handler',
