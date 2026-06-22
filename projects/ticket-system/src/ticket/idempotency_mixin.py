from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from .models import IdempotencyKey


class IdempotentCreateMixin:
    """
    Mixin para ViewSets que asegura idempotencia usando Idempotency-Key.
    """

    def create(self, request, *args, **kwargs):
        key = request.headers.get("Idempotency-Key")
        user = request.user
        endpoint = request.path

        # Si no hay key, simplemente procesamos el request
        if not key:
            return super().create(request, *args, **kwargs)

        # Buscamos si la key ya existe
        record = IdempotencyKey.objects.filter(
            key=key, user=user, endpoint=endpoint
        ).first()

        if record:
            # Ya existe, devolvemos la respuesta anterior
            return Response(record.response_body, status=record.response_status)

        # Procesamos el request normalmente y guardamos el resultado
        try:
            with transaction.atomic():
                response = super().create(request, *args, **kwargs)

                # Guardamos la key y la respuesta
                IdempotencyKey.objects.create(
                    key=key,
                    user=user,
                    endpoint=endpoint,
                    response_status=response.status_code,
                    response_body=response.data,
                )

                return response

        except IntegrityError:
            # Caso raro: dos requests simultáneos con la misma key
            record = IdempotencyKey.objects.get(key=key, user=user, endpoint=endpoint)
            return Response(record.response_body, status=record.response_status)

