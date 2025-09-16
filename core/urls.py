from django.urls import path
from . import views

urlpatterns = [
    path("resident-archive/", views.resident_archive, name="resident_archive"),
    path("reactivate-resident/<int:resident_id>/", views.reactivate_resident, name="reactivate_resident"),
]
