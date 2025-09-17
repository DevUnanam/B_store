from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import StorageUnit, StorageRequest
from .forms import StorageUnitForm
from users.decorators import role_required
from django.db.models import Count

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

@role_required(allowed_roles=["tenant"])
def request_unit(request, pk):
    unit = get_object_or_404(StorageUnit, pk=pk, status="available")
    # prevent duplicate requests
    if StorageRequest.objects.filter(resident=request.user, unit=unit, status="pending").exists():
        messages.error(request, "You already requested this unit.")
    else:
        StorageRequest.objects.create(resident=request.user, unit=unit)
        messages.success(request, f"Request for {unit.name} submitted.")
    return redirect("available_units")

# Admin: manage requests
@role_required(allowed_roles=["admin"])
def manage_requests(request):
    requests = StorageRequest.objects.select_related("resident", "unit").order_by("-created_at")
    return render(request, "storage/manage_requests.html", {"requests": requests})

# Admin: approve request
@role_required(allowed_roles=["admin"])
def approve_request(request, pk):
    req = get_object_or_404(StorageRequest, pk=pk, status="pending")
    req.status = "approved"
    req.unit.status = "occupied"
    req.unit.save()
    req.save()
    messages.success(request, f"Request approved. {req.unit.name} assigned to {req.resident.username}.")
    return redirect("manage_requests")

# Admin: reject request
@role_required(allowed_roles=["admin"])
def reject_request(request, pk):
    req = get_object_or_404(StorageRequest, pk=pk, status="pending")
    req.status = "rejected"
    req.save()
    messages.warning(request, f"Request rejected for {req.unit.name}.")
    return redirect("manage_requests")

@role_required(allowed_roles=["tenant"])
def my_requests(request):
    requests = StorageRequest.objects.filter(resident=request.user).order_by("-requested_at")
    return render(request, "storage/my_requests.html", {"requests": requests})

@role_required(allowed_roles=["tenant"])
def resident_dashboard(request):
    resident = request.user.resident_profile

    # Find current active request (approved & not released)
    current_request = StorageRequest.objects.filter(
        resident=resident, status="approved"
    ).first()

    # All past requests
    history = StorageRequest.objects.filter(resident=resident).order_by("-created_at")

    return render(
        request,
        "storage/resident_dashboard.html",
        {"current_request": current_request, "history": history},
    )


@role_required(allowed_roles=["tenant"])
def release_unit(request, pk):
    storage_request = get_object_or_404(StorageRequest, pk=pk, resident=request.user.resident_profile)

    if storage_request.status == "approved":
        storage_request.release()
        messages.success(request, "You have successfully released the storage unit.")
    else:
        messages.error(request, "This unit cannot be released.")

    return redirect("resident_dashboard")

@role_required(allowed_roles=["admin"])
def admin_dashboard(request):
    # Reports
    report = {
        "available_units": StorageUnit.objects.filter(status="available").count(),
        "occupied_units": StorageUnit.objects.filter(status="occupied").count(),
        "maintenance_units": StorageUnit.objects.filter(status="maintenance").count(),
        "total_units": StorageUnit.objects.count(),
    }

    # All storage units (with assigned resident if any)
    units = StorageUnit.objects.select_related("assigned_to").all()

    # Requests (pending + approved + rejected)
    requests = StorageRequest.objects.select_related("resident", "unit").order_by("-created_at")

    # Released units (filter by those that have a released_at timestamp)
    released_units = StorageUnit.objects.filter(released_at__isnull=False).order_by("-released_at")

    context = {
        "report": report,
        "units": units,
        "requests": requests,
        "released_units": released_units,
    }
    return render(request, "storage/admin_dashboard.html", context)