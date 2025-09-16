# storage/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.storage_admin_dashboard, name="storage_admin_dashboard"),
    path("admin-dashboard/add/", views.add_storage_unit, name="add_storage_unit"),
    path("available/", views.available_units, name="available_units"),
    path("admin-dashboard/edit/<int:pk>/", views.edit_storage_unit, name="edit_storage_unit"),
    path("admin-dashboard/delete/<int:pk>/", views.delete_storage_unit, name="delete_storage_unit"),
    path("request/<int:pk>/", views.request_unit, name="request_unit"),
    path("requests/", views.manage_requests, name="manage_requests"),
    path("requests/approve/<int:request_id>/", views.approve_request, name="approve_request"),
    path("requests/deny/<int:request_id>/", views.reject_request, name="deny_request"),
    path("my-requests/", views.my_requests, name="my_requests"),
]
