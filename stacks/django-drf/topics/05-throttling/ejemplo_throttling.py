# Ejemplo: Throttling en DRF

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

# -------------------------------------------------#
# Ejemplo 1: Throttling global en settings.py
# -------------------------------------------------#
"""
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',   # 20 requests por minuto para anónimos
    },
}
"""


# -------------------------------------------------#
# Ejemplo 2: Throttling por vista
# -------------------------------------------------#
from rest_framework.generics import ListAPIView

class TaskListView(ListAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # Si no se especifica rate, usa la configuración global


# -------------------------------------------------#
# Ejemplo 3: Custom Throttle
# -------------------------------------------------#
from rest_framework.throttling import SimpleRateThrottle

class BurstRateThrottle(SimpleRateThrottle):
    """Limita a 10 requests por minuto"""
    scope = 'burst'
    
    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    
    def get_rate(self):
        return '10/minute'


# -------------------------------------------------#
# Ejemplo 4: Throttling por acción en ViewSet
# -------------------------------------------------#
"""
from rest_framework.viewsets import ModelViewSet

class TaskViewSet(ModelViewSet):
    def get_throttles(self):
        if self.action == 'list':
            return [UserRateThrottle()]
        return []
"""
