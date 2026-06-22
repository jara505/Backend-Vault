from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    response_status = models.PositiveSmallIntegerField()
    response_body = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("key", "user", "endpoint")
        indexes = [
            models.Index(fields=["key", "user"]),
        ]

    def __str__(self):
        return f"IdempotencyKey: {self.key} for {self.user}"

