# Querysets Dinámicos: get_queryset() y Filtrado por Usuario/Contexto

## ¿Qué es?
En DRF, `get_queryset()` es un método en vistas genéricas (como `ListAPIView`) que permite definir el queryset dinámicamente basado en el contexto de la request (ej. usuario autenticado, query params).

## Por qué usarlo?
- **Filtrado seguro:** Evita que usuarios vean datos de otros (ej. tickets de otros users).
- **Performance:** Filtra en DB, no en Python.
- **Flexibilidad:** Cambia queryset por request (ej. admin ve todo, user solo lo suyo).

## Ejemplo Aplicado a Tickets
Ver `ejemplo_get_queryset.py` para código.

### Cómo integrarlo al proyecto:
1. En `src/ticket/views.py`, modifica `TicketListView`:
   ```python
   def get_queryset(self):
       return Ticket.objects.filter(created_by=self.request.user)
   ```
2. Prueba: GET `/api/tickets/` con JWT. Solo tus tickets.

### Mejores Prácticas
- Usa `select_related()`/`prefetch_related()` para joins.
- Para filtros avanzados: integra `django-filter` en la siguiente subunidad.
- Evita lógica compleja; si es mucha, mueve a manager de modelo.

## Recursos
- [DRF Docs: Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [Django Querysets](https://docs.djangoproject.com/en/stable/ref/models/querysets/)