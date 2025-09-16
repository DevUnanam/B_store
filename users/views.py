from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseForbidden
from users.models import CustomUser
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileUpdateForm

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, "This account is deactivated. To reactivate, kindly contact admin")
                return redirect("login")
            login(request, user)
            return redirect("dashboard")
        else:
            form = CustomLoginForm()
            return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")


def is_admin(user):
    return user.is_authenticated and user.role == "admin"

@login_required
@user_passes_test(is_admin)
def deactivate_user(request, user_id):
   user_to_deactivate = get_object_or_404(CustomUser, id=user_id, role="occupant")
   user_to_deactivate.soft_delete()
   return redirect("dashboard")

@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def resident_list(request):
    residents = CustomUser.objects.filter(role="occupant")
    return render(request, "users/resident_list.html", {"residents": residents})

@login_required
@user_passes_test(is_admin)
def toggle_resident_status(request, user_id):
    resident = get_object_or_404(CustomUser, id=user_id, role="occupant")
    resident.is_active = not resident.is_active  # Toggle active status
    resident.save()
    return redirect("users:resident_list")
