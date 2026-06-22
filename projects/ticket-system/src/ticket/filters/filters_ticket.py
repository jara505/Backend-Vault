import django_filters as filters
from ..models.ticket import Ticket

"""
gte -> Greater than or equal (>=)
gt -> mayor que
lte -> Less than or equal (<=)
lt -> menor que

"""

"""
Este tecnica se llama: declarar filtros en un FilterSet con nombres públicos distintos al modelo / desacoplar o abstraccion a nivel de API
Podemos utilizar FileSet sin niguna declaracion de filtros publicos si son proyectos pequenos.

Si necesitamos control y el uso de lookup_expri, modelos que sean mantenibles o que puedan cambiar entonces usamos declaracion de filtros publicos
"""


class TicketFilter(filters.FilterSet):
    # filtrar por la minima
    estado = filters.CharFilter(field_name="status", lookup_expr="exact")
    min_priority = filters.NumberFilter(field_name="priority__gte", lookup_expr="gte")

    class Meta:
        model = Ticket
        # fields = ["title", "created_by", "status"]
        fields = []
