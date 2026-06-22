from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination


class TicketPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
