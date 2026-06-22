# Filtrado Avanzado con `django-filter`

`django-filter` es la librería estándar para crear APIs de Django REST Framework (DRF) que permitan un filtrado de datos robusto, declarativo y seguro. Se integra de forma nativa con los ViewSets y las vistas genéricas de DRF.

## 1. `FilterSet`: El Corazón del Filtrado

El `FilterSet` es una clase que define cómo los parámetros de una URL (`query params`) se traducen en consultas (`queries`) a la base de datos sobre un `queryset` de Django.

### ¿Por qué `FilterSet` en lugar de `filterset_fields`?

- **Control Explícito:** `filterset_fields` es un atajo que crea filtros básicos automáticamente. Aunque útil para prototipos, ofrece poco control. Un `FilterSet` declarativo te permite:
    - Definir el tipo de filtro exacto (`CharFilter`, `NumberFilter`, etc.).
    - Personalizar el `lookup_expr` (ej. `icontains` en lugar de `exact`).
    - Desacoplar el nombre del `query param` del nombre del campo en el modelo.
    - Añadir filtros que no mapean directamente a un campo del modelo.

- **Mantenibilidad y Claridad:** Un `FilterSet` es auto-documentado. Cualquiera que lo lea sabe exactamente qué filtros están disponibles y cómo se comportan.

### Conexión con la Vista

Para que una vista de DRF utilice tu `FilterSet`, debes conectarlos de la siguiente manera:

1.  Añade `DjangoFilterBackend` a la lista de `filter_backends` de la vista.
2.  Especifica tu clase `FilterSet` en el atributo `filterset_class`.

```python
# views.py
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .filters import TicketFilter
from .serializers import TicketSerializer
from rest_framework import viewsets

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all() # Queryset base
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter
```

### La Importancia del `queryset` Base

DRF y `django-filter` necesitan un punto de partida antes de aplicar cualquier filtro. Este es el `queryset` base.

- **`queryset` (atributo de clase):** Define el conjunto de datos sobre el cual se aplicarán los filtros. Es la opción más común y sencilla.
- **`get_queryset()` (método):** Ofrece la capacidad de construir un `queryset` dinámico. Es aquí donde se deben aplicar filtros de seguridad o de dominio que **no son opcionales**. Por ejemplo, filtrar los tickets que pertenecen al usuario autenticado.

```python
# En un ViewSet
def get_queryset(self):
    # Filtro de seguridad: solo los tickets del usuario actual.
    return Ticket.objects.filter(owner=self.request.user)
```

## 2. Filtros Básicos Declarativos

Dentro de un `FilterSet`, cada atributo es un filtro. Los más comunes son:

- **`CharFilter`:** Para campos de texto.
- **`NumberFilter`:** Para campos numéricos (`IntegerField`, `DecimalField`, etc.).
- **`BooleanFilter`:** Para campos `BooleanField`.

```python
# filters.py
from django_filters import rest_framework as filters
from .models import Ticket

class TicketFilter(filters.FilterSet):
    # Filtra tickets cuyo título contenga el valor (insensible a mayúsculas).
    title = filters.CharFilter(lookup_expr='icontains')

    # Filtra por un valor numérico exacto.
    priority = filters.NumberFilter(lookup_expr='exact')

    # Renombra el query param a 'min_priority' para mayor claridad.
    priority_min = filters.NumberFilter(field_name='priority', lookup_expr='gte')
    priority_max = filters.NumberFilter(field_name='priority', lookup_expr='lte')

    class Meta:
        model = Ticket
        # 'status' usará el filtro por defecto (CharFilter con 'exact').
        fields = ['title', 'priority', 'status']
```

- **`field_name`:** Permite que el nombre del `query param` en la URL (ej. `min_priority`) sea diferente del campo en el modelo (`priority`). Esto es clave para diseñar APIs limpias y desacopladas.
- **`lookup_expr`:** Especifica el operador de consulta del ORM de Django (`exact`, `icontains`, `gte`, `lte`, etc.).

## 3. Aplicación sobre `Querysets`

El `DjangoFilterBackend` se encarga de la magia:

- **Si hay `query params`:** Inspecciona la URL, encuentra los parámetros que coinciden con los filtros definidos en el `FilterSet` y los aplica al `queryset` base.
    - `GET /api/tickets/?status=open&min_priority=3` -> Devuelve tickets abiertos con prioridad >= 3.
- **Si no hay `query params`:** Simplemente devuelve el `queryset` base sin modificar.
    - `GET /api/tickets/` -> Devuelve todos los tickets (o los del `get_queryset()` si está definido).
- **Si un `param` no existe en el `FilterSet`:** Es ignorado silenciosamente. Esto evita errores por parámetros inesperados y permite flexibilidad.
    - `GET /api/tickets/?param_inesperado=valor` -> `param_inesperado` se ignora.

## 4. Buenas Prácticas

- **Seguridad en `get_queryset()`:** Los filtros que garantizan que un usuario solo vea los datos que le corresponden **siempre** deben ir en `get_queryset()`. Nunca dependas de que el cliente envíe el `user_id` correcto en un `query param`.
- **No expongas el ORM:** Usa `field_name` para crear una API pública limpia y no acoples tus `query params` a los nombres de tus campos de la base de datos. Evita exponer operadores complejos directamente.
- **Un `FilterSet` por dominio:** No crees múltiples `FilterSet` para el mismo modelo. Consolida toda la lógica de filtrado de un recurso (ej. `Ticket`) en una sola clase (`TicketFilter`).
- **Filtros opcionales por defecto:** Todos los filtros son opcionales. Si un `query param` no se incluye, el filtro no se aplica. Para hacerlo obligatorio, puedes usar `required=True` en la definición del filtro, aunque esto es menos común en APIs REST.

## 5. Uso Combinado con DRF

La integración es transparente. `DjangoFilterBackend` actúa como un intermediario entre la URL, tu `FilterSet` y el `queryset` de la vista.

- **Sin tocar `urls.py`:** No necesitas definir los `query params` en tus patrones de URL. DRF los gestiona automáticamente.
- **Compatibilidad con Vistas Genéricas y `ViewSets`:** Funciona perfectamente con `ListAPIView`, `ModelViewSet`, etc., sin necesidad de código adicional.
- **Documentación Automática:** Herramientas como `drf-spectacular` pueden inspeccionar tu `FilterSet` y generar automáticamente la documentación de la API, incluyendo todos los `query params` disponibles.
