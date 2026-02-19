# Permisos Avanzados en DRF

Los permisos controlan quién puede acceder a qué. DRF ofrece un sistema flexible para manejar autorización a diferentes niveles.

## ¿Por qué permisos avanzados?

- **Seguridad:** Distingue entre usuarios, admins, managers.
- **Granularidad:** Permisos por acción (list vs destroy).
- **Lógica de negocio:** Reglas custom basadas en el contexto.

## Sistema de Permisos en DRF

### Cómo funciona

1. Las vistas declaran `permission_classes`
2. DRF verifica cada permission en orden
3. Si cualquiera retorna `False`, acceso denegado
4. Por defecto, si no hay permissions, se permite todo

### Permisos Includeos

| Permission | Descripción |
|------------|-------------|
| `AllowAny` | Permite todos los requests |
| `IsAuthenticated` | Requiere usuario logueado |
| `IsAdminUser` | Solo admins (is_staff=True) |
| `IsAuthenticatedOrReadOnly` | Autenticado o solo lectura |

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class TicketListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados
```

## Permisos Personalizados (Custom Permissions)

### Permission Basic

```python
from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff  # o request.user.groups.filter(name='manager').exists()
```

### Permission con Métodos HTTP

```python
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lectura permitida a cualquiera
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Escritura solo al owner
        return obj.owner == request.user
```

## Permisos por Acción

### En ViewSets

```python
from rest_framework.viewsets import ModelViewSet

class TaskViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdminUser()]
        elif self.action == 'close':
            return [IsAdminUser()]  # Acción custom
        return [IsAuthenticated()]
```

### Con decoradores en acciones custom

```python
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

class TaskViewSet(ModelViewSet):
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def close(self, request, pk=None):
        # Solo admins pueden cerrar tareas
        ...
```

## Permisos a Nivel de Objeto (Object-Level)

Usá `has_object_permission` para controlar acceso a objetos específicos:

```python
class TicketViewSet(ModelViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]  # Permiso general
    
    def get_object(self):
        obj = super().get_object()
        # Verificación adicional de ownership
        if obj.created_by != self.request.user:
            self.permission_denied(request)
        return obj
```

## Ejemplo: Permission Combinada con Ownership

```python
from rest_framework.permissions import BasePermission

class IsTicketOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_staff
```

## Mejores Prácticas

1. **Orden de permisos importa:** DRF evalúa en orden
2. **Usa `has_object_permission`:** Para detalle de objetos
3. **Separa permisos de lógica de negocio:** No mezcles autorización con validación
4. **Throws: 403 Forbidden:** Cuando no tenés permiso

## Ejemplo del Proyecto

```python
# src/tasks/permissions/permissions.py
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.decorators import action

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class TaskViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        elif self.action == "destroy":
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def close(self, request, pk=None):
        ...
```

## Recursos

- [DRF Permissions Docs](https://www.django-rest-framework.org/api-guide/permissions/)
