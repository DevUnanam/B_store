from django.urls import path
from .views import deactivate_user, edit_profile, profile_view, register_view, login_view, logout_view, resident_list, toggle_resident_status

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("deactivate/<int:user_id>/", deactivate_user, name="deactivate_user"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("residents/", resident_list, name="resident_list"),
    path("residents/toggle/<int:user_id>/", toggle_resident_status, name="toggle_resident_status"),
]
