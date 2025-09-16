from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from users.models import CustomUser, Resident

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def landing_page(request):
    return render(request, "core/landing.html")

@login_required
def dashboard(request):
    role = request.user.role
    if role == "admin":
        occupants = CustomUser.objects.filter(role="occupant")
        return render(request, "core/dashboard.html", {"occupants": occupants})
        # message = "Welcome Admin! You can manage storage units."
    else:
        return render(request, "core/occupant_dashboard.html")


@login_required
@user_passes_test(is_admin)
def resident_archive(request):
    archived_residents = Resident.objects.filter(is_active=False).order_by("-deactivated_at")
    return render(request, "core/resident_archive.html", {"archived_residents": archived_residents})

@login_required
@user_passes_test(is_admin)
def reactivate_resident(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id, is_active=False)
    resident.activate()
    messages.success(request, f"Resident {resident.name} has been reactivated.")
    return redirect("resident_archive")