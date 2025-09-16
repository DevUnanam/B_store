from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Resident(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resident_profile"
    )
    name = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_active = models.BooleanField(default=True)  # soft delete
    deactivated_at = models.DateTimeField(blank=True, null=True)  # NEW field

    def deactivate(self):
        self.is_active = False
        self.deactivated_at = timezone.now()
        self.save()

    def activate(self):
        self.is_active = True
        self.deactivated_at = None
        self.save()

    def __str__(self):
        return f"{self.name} - Apt {self.apartment_number}"


class StorageUnit(models.Model):
    SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    name = models.CharField(max_length=100, unique=True)  # e.g. Locker A1
    location = models.CharField(max_length=255)  # e.g. Basement B3
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="medium")
    is_available = models.BooleanField(default=True)

    assigned_to = models.ForeignKey(
        Resident,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="storage_units"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def assign_to(self, resident):
        """Assign unit to a resident and mark unavailable"""
        self.assigned_to = resident
        self.is_available = False
        self.save()

    def release(self):
        """Release unit back to available"""
        self.assigned_to = None
        self.is_available = True
        self.save()

    def __str__(self):
        return f"{self.name} ({self.size}) - {'Available' if self.is_available else 'Occupied'}"