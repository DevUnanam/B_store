from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resident_profile")
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
