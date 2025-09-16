# storage/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import StorageUnit
from .forms import StorageUnitForm
from users.decorators import role_required

@role_required(allowed_roles=["admin"])
def storage_admin_dashboard(request):
    units = StorageUnit.objects.all()
    return render(request, "storage/admin_dashboard.html", {"units": units})

@role_required(allowed_roles=["admin"])
def add_storage_unit(request):
    if request.method == "POST":
        form = StorageUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("storage_admin_dashboard")
    else:
        form = StorageUnitForm()
    return render(request, "storage/add_unit.html", {"form": form})

@role_required(allowed_roles=["admin"])
def edit_storage_unit(request, pk):
    unit = get_object_or_404(StorageUnit, pk=pk)
    if request.method == "POST":
        form = StorageUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect("storage_admin_dashboard")
    else:
        form = StorageUnitForm(instance=unit)
    return render(request, "storage/edit_unit.html", {"form": form, "unit": unit})

@role_required(allowed_roles=["admin"])
def delete_storage_unit(request, pk):
    unit = get_object_or_404(StorageUnit, pk=pk)
    unit.delete()
    messages.success(request, "Storage unit deleted successfully.")
    return redirect("storage_admin_dashboard")

@role_required(allowed_roles=["tenant"])
def available_units(request):
    units = StorageUnit.objects.filter(status="available")
    return render(request, "storage/available_units.html", {"units": units})
