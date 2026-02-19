from django.conf import settings
from django.db import models
from ..choices import UserRole

User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
    )

    def __str__(self):
        return f"{self.user} ({self.role})"
