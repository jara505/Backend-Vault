# Paginación en DRF

La paginación es esencial para APIs que devuelven grandes cantidades de datos. DRF ofrece varias estrategias de paginación integradas.

## ¿Por qué usarla?

- **Performance:** Evita devolver miles de registros en una sola request.
- **UX:** Facilita el consumo en frontend (listas infinitas, páginas).
- **Cost:** Reduce el uso de memoria y ancho de banda.

## Tipos de Paginación en DRF

### 1. `LimitOffsetPagination` (Más común)

Ideal para APIs donde el cliente especifica cuántos datos quiere y desde dónde.

```python
# src/tasks/pagination/task_pagination.py
from rest_framework.pagination import LimitOffsetPagination

class TaskPagination(LimitOffsetPagination):
    default_limit = 5   # Registros por defecto
    max_limit = 20     # Límite máximo que el cliente puede pedir
```

**Uso en vista:**
```python
from rest_framework.generics import ListAPIView
from tasks.pagination.task_pagination import TaskPagination

class TaskListView(ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    queryset = Task.objects.all()
```

**Request:**
```
GET /api/tasks/?limit=10&offset=20
```

**Response:**
```json
{
    "count": 100,
    "next": "http://api/tasks/?limit=10&offset=30",
    "previous": "http://api/tasks/?limit=10&offset=10",
    "results": [...]
}
```

### 2. `PageNumberPagination`

Para interfaces tradicionales con números de página (1, 2, 3...).

```python
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_query_param = 'page'
    max_page_size = 1000
```

**Request:**
```
GET /api/tasks/?page=2
```

### 3. `CursorPagination` (Más eficiente para datos masivos)

Usa cursores en lugar de offsets. Ideal para datos que cambian frecuentemente o tablas enormes.

```python
from rest_framework.pagination import CursorPagination

class CursorSetPagination(CursorPagination):
    page_size = 25
    ordering = '-created_at'
```

## Configuración Global

En `settings.py` podés aplicar paginación por defecto a todas las vistas:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}
```

## Cuándo usar cuál?

| Tipo | Cuándo usarlo |
|------|---------------|
| `LimitOffsetPagination` | APIs modernas, dashboards, CRUD estándar |
| `PageNumberPagination` | UI clásica con números de página |
| `CursorPagination` | Listas infinitas, datos masivos, alto rendimiento |

## Ejemplo Integrdo al Proyecto

```python
# src/ticket/pagination/pagination.py
from rest_framework.pagination import LimitOffsetPagination

class TicketPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20

# src/ticket/views.py
from .pagination.pagination import TicketPagination

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    pagination_class = TicketPagination
    
    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)
```

## Recursos

- [DRF Pagination Docs](https://www.django-rest-framework.org/api-guide/pagination/)
