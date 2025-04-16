from datetime import timedelta

from django.db import models
from django.utils import timezone


class OTP(models.Model):
    phone_number = models.CharField(
        max_length=15,
    )

    code = models.CharField(
        max_length=6,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.phone_number} - {self.code}'

    @property
    def is_expired(self):
        """Check if the OTP is older than 5 minutes"""
        return timezone.now() > self.created_at + timedelta(minutes=5)
