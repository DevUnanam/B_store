from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("occupant", "Occupant"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="occupant")
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        """Deactivate user but retain record"""
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.username} ({self.role})"
