# Unidad 1: DRF Intermedio (Filtrado, Seguridad y Performance)

## Objetivo
Crear APIs robustas, seguras y eficientes aplicadas al proyecto de tickets. Enfocándonos en querysets dinámicos y serializers avanzados.

## Subunidades Cubiertas
- **Querysets Dinámicos:** `get_queryset()` y filtrado por usuario/contexto.
- **Serializers Avanzados:** Fields read-only/write-only, validaciones cross-field, SerializerMethodField.
- **Filtrado y Búsqueda:** `django-filter`, `SearchFilter` y `OrderingFilter`.
- **Paginación:** `LimitOffsetPagination`, `PageNumberPagination`, `CursorPagination`.
- **Throttling:** Rate limiting global y por vista, custom throttles.
- **Permisos Avanzados:** Custom permissions, permisos por acción, object-level permissions.
- **Error Handling:** Custom exception handler, excepciones de negocio, validation errors.

## Cómo Usar
1. Lee las explicaciones en cada subcarpeta.
2. Copia/ejecuta los ejemplos en `src/ticket/`.
3. Prueba con `python src/manage.py runserver` y APIs de tickets.
4. Integra al código real para practicar.

## Próximas Subunidades (no incluidas aquí)
- Acciones custom.
- Testing APIs.

## Notas
- Estos demos son básicos; expándelos para lógica compleja.
- Siempre testea permisos y performance.