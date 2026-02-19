# Throttling (Rate Limiting) en DRF

El throttling controla cuántos requests puede hacer un usuario en un período de tiempo. Esencial para prevenir abuse de tu API.

## ¿Por qué usarlo?

- **Prevención de abuse:** Evita que un cliente haga miles de requests por segundo.
- **Protección de recursos:** Mantiene la estabilidad del servidor.
- **Fairness:** Asegura que todos los clientes tengan acceso equitativo.

## Tipos de Throttling en DRF

### 1. Throttling Global (Settings)

Aplica a toda la API:

```python
# src/core/settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',      # Usuarios anónimos: 20 req/min
        'user': '100/minute',     # Usuarios autenticados: 100 req/min
    },
}
```

### 2. Throttling por Vista

Aplicá throttling específico a ciertas vistas:

```python
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class TaskListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # ...
```

### 3. Custom Throttles

Creá tus propias reglas de throttling:

```python
# src/tasks/throttling/throttling.py
from rest_framework.throttling import SimpleRateThrottle

class BurstRateThrottle(SimpleRateThrottle):
    scope = 'burst'
    get_rate = lambda self, n, d: ('10/minute')  # 10 req/min

class SustainedRateThrottle(SimpleRateThrottle):
    scope = 'sustained'
    get_rate = lambda self, n, d: ('1000/day')  # 1000 req/día
```

## Throttles Incluidos en DRF

| Throttle | Descripción |
|----------|-------------|
| `AnonRateThrottle` | Limita requests por IP (para anonimos) |
| `UserRateThrottle` | Limita requests por usuario autenticado |
| `ScopedRateThrottle` | Limita por acción específica |

## Ejemplo: Throttling por Acción

```python
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle

class TaskViewSet(ModelViewSet):
    @throttle_classes([UserRateThrottle])
    def list(self, request, *args, **kwargs):
        # Límite específico para list
        return super().list(request, *args, **kwargs)
    
    @throttle_classes([])  # Sin límite para create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
```

## Cómo funciona el cache

DRF usa el cache de Django para tracking. Asegurate de tener cache configurado:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

## Ejemplo Configuración Actual del Proyecto

```python
# src/core/settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.AnonRateThrottle',),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',
    },
}
```

Esto limita usuarios anónimos a 20 requests por minuto.

## Errores Comunes

- **Rate no válido:** Debe seguir formato `'num/period'` (ej. `'100/hour'`)
- **Sin cache configurado:** El throttling no funciona correctamente
- **Throttling muy agresivo:** Puede bloquear clientes legítimos

## Recursos

- [DRF Throttling Docs](https://www.django-rest-framework.org/api-guide/throttling/)
