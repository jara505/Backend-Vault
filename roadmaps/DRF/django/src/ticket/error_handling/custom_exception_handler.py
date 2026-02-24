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


# Registrar en settings.py:
# REST_FRAMEWORK = {
#     "EXCEPTION_HANDLER": "ticket.error_handling.custom_exception_handler.custom_exception_handler",
# }
