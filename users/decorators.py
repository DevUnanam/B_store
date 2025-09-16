from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    """
    Restrict view access based on user.role
    Usage: @role_required(["admin"])
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.role not in allowed_roles:
                raise PermissionDenied  # or redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
