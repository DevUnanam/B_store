from django.contrib import admin
from .models import Resident, StorageUnit

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("name", "apartment_number", "contact", "is_active")
    list_filter = ("is_active",)

@admin.register(StorageUnit)
class StorageUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "size", "is_available", "assigned_to")
    list_filter = ("is_available", "size")
    search_fields = ("name", "location")
