# storage/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.storage_admin_dashboard, name="storage_admin_dashboard"),
    path("admin-dashboard/add/", views.add_storage_unit, name="add_storage_unit"),
    path("available/", views.available_units, name="available_units"),
    path("admin-dashboard/edit/<int:pk>/", views.edit_storage_unit, name="edit_storage_unit"),
    path("admin-dashboard/delete/<int:pk>/", views.delete_storage_unit, name="delete_storage_unit"),
]
