from django.conf import settings
from django.db import models
from ..choices import TicketStatus

User = settings.AUTH_USER_MODEL


class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets_created",
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets_assigned",
    )

    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
    )
    priority = models.PositiveSmallIntegerField(default=3)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"[{self.status}] {self.title}"
