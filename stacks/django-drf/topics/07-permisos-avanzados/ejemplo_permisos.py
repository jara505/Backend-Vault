# Ejemplo: Permisos Avanzados en DRF

from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

# -------------------------------------------------#
# Ejemplo 1: Custom Permission básica
# -------------------------------------------------#

class IsManager(BasePermission):
    """Permite solo a usuarios staff (managers)"""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# -------------------------------------------------#
# Ejemplo 2: Permission con lógica por método HTTP
# -------------------------------------------------#

class IsOwnerOrReadOnly(BasePermission):
    """
    - GET, HEAD, OPTIONS: cualquiera puede leer
    - PUT, DELETE: solo el owner puede modificar/eliminar
    """
    def has_object_permission(self, request, view, obj):
        # Lectura libre
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        
        # Escritura solo al owner
        return obj.owner == request.user


# -------------------------------------------------#
# Ejemplo 3: Permisos por acción en ViewSet
# -------------------------------------------------#

class TaskViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdminUser()]
        elif self.action == 'close':
            return [IsAdminUser()]  # Acción custom
        return [IsAuthenticated()]


# -------------------------------------------------#
# Ejemplo 4: Acción custom con permission_classes
# -------------------------------------------------#

from rest_framework.decorators import action

class TaskViewSet(ModelViewSet):
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def close(self, request, pk=None):
        """Solo admins pueden cerrar tareas"""
        task = self.get_object()
        task.status = 'closed'
        task.save()
        return Response({'status': 'task closed'})


# -------------------------------------------------#
# Ejemplo 5: Permission con grupos
# -------------------------------------------------#

class IsAdminGroup(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='admin').exists()


# -------------------------------------------------#
# Ejemplo 6: Combinando permissions
# -------------------------------------------------#

from rest_framework.permissions import AND, OR

# DRF evaluará en orden: IsAuthenticated primero, luego IsManager
# Si cualquiera falla, acceso denegado
class TaskListView(ModelViewSet):
    permission_classes = [IsAuthenticated, IsManager]
