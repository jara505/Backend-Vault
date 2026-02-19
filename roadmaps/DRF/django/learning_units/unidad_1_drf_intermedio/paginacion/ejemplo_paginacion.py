# Ejemplo: Paginación en DRF
# Aplicado al proyecto de tareas

from rest_framework.pagination import LimitOffsetPagination

# -------------------------------------------------#
# Ejemplo 1: LimitOffsetPagination (usado en el proyecto)
# -------------------------------------------------#

class TaskPagination(LimitOffsetPagination):
    default_limit = 5    # Por defecto 5 registros
    max_limit = 20       # Máximo que puede pedir el cliente

# Uso en una vista
"""
from rest_framework.generics import ListAPIView
from tasks.models import Task
from tasks.serializers import TaskSerializer

class TaskListView(ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    queryset = Task.objects.all()
"""

# Request: GET /api/tasks/?limit=10&offset=20
# Response: {"count": 100, "next": "...", "previous": "...", "results": [...]}


# -------------------------------------------------#
# Ejemplo 2: PageNumberPagination
# -------------------------------------------------#
from rest_framework.pagination import PageNumberPagination

class TaskPagePagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 100

# Request: GET /api/tasks/?page=2


# -------------------------------------------------#
# Ejemplo 3: Configuración global en settings.py
# -------------------------------------------------#
"""
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}
"""
