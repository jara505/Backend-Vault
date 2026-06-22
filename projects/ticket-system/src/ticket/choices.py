from django.db import models


class UserRole(models.TextChoices):
    USER = "user", "User"
    AGENT = "agent", "Agent"
    ADMIN = "admin", "Admin"


class TicketStatus(models.TextChoices):
    OPEN = "open", "Open"
    IN_PROGRESS = "in_progress", "In progress"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"
