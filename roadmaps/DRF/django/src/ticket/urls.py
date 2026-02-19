from django.urls import path
from .views import (
    TicketCreateView,
    TicketFilterActivate,
    TicketListView,
    TicketFilterSetView,
)


urlpatterns = [
    path("", TicketListView.as_view(), name="ticket-list"),
    path("create/", TicketCreateView.as_view(), name="ticket-create"),
    path("activate/", TicketFilterActivate.as_view(), name="filter_activate"),
    path("filtro/", TicketFilterSetView.as_view(), name="filter"),
]
