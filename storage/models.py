# storage/models.py
from django.db import models

class StorageUnit(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("occupied", "Occupied"),
        ("maintenance", "Under Maintenance"),
    ]

    name = models.CharField(max_length=100, unique=True)  # e.g. Locker A1, Basement B3
    size = models.CharField(max_length=50)  # e.g. Small, Medium, Large
    location = models.CharField(max_length=100)  # e.g. Basement, Floor 2
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
