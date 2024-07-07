# decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def admin_required(function):
    """
    Decorator for views that checks that the user is an admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/web/login/staff/'  # Redirect to login page if user is not admin
    )
    return actual_decorator(function)
